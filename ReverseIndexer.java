/**
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 */



import java.io.IOException;
import java.util.HashMap;
import java.util.ArrayList;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.lib.input.FileSplit;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.GenericOptionsParser;



public class ReverseIndexer {


    public static class IndexerMapper
            extends Mapper<LongWritable, Text, Text, LineRecWritable>{

        private Text word = new Text();
        private int lineNum = 0;

        public void map(LongWritable key, Text value, Context context
        ) throws IOException, InterruptedException {
            int position = 0;
            FileSplit fileSplit = (FileSplit)context.getInputSplit();
            String filename = fileSplit.getPath().getName();
            String[] lines = value.toString().split("(-|\\s)+");
            // use the first token as the value, then all the others as keys
            lineNum = Integer.parseInt(lines[0]);
            for (int i = 1; i < lines.length; i++) {
                word.set(lines[i].replaceAll("[^A-Za-z]", "").toLowerCase());
                context.write(word, new LineRecWritable(filename, lineNum, position));
                position++;
            }
        }
    }

    public static class IndexerReducer
            extends Reducer<Text,LineRecWritable,Text,Text> {

        private Text out = new Text();

        public void reduce(Text key, Iterable<LineRecWritable> values,
                           Context context
        ) throws IOException, InterruptedException {
            HashMap<String, ArrayList<String>> fileLines = new HashMap<String, ArrayList<String>>();
            String lines = "";
            int wordCount = 0;

            Configuration conf = context.getConfiguration();
            int threshold = conf.getInt("threshold", 50);

            for (LineRecWritable lineRec : values) {
                String filename = lineRec.getFilename();
                String position = lineRec.getLineNum() + ":" + lineRec.getPos();
                if (fileLines.containsKey(filename)) {
                    fileLines.get(filename).add(position);
                } else {
                    ArrayList<String> positions = new ArrayList<String>();
                    positions.add(position);
                    fileLines.put(filename, positions);
                }
                wordCount++;
            }

            if (wordCount < threshold) {
                for (String filename : fileLines.keySet()) {
                    lines += filename;
                    for (String position : fileLines.get(filename)) {
                        lines += "," + position;
                    }
                    lines += "\t";
                }
                out.set(lines);
                context.write(key, out);
            }
        }
    }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        String[] otherArgs = new GenericOptionsParser(conf, args).getRemainingArgs();
        if (otherArgs.length < 2) {
            System.err.println("Usage: ReverseIndexer <output> <input file(s)>");
            System.exit(2);
        }
        conf.setInt("threshold", 5);
        Job job = new Job(conf, "reverse indexer");
        job.setJarByClass(ReverseIndexer.class);
        job.setMapperClass(IndexerMapper.class);
        job.setReducerClass(IndexerReducer.class);
        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(LineRecWritable.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);
        for (int i = 1; i < otherArgs.length; i++) {
            FileInputFormat.addInputPath(job, new Path(otherArgs[i]));
        }
        FileOutputFormat.setOutputPath(job, new Path(otherArgs[0]));
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
