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
import java.util.StringTokenizer;

import java.io.IOException;
import java.util.StringTokenizer;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.TextInputFormat;
import org.apache.hadoop.mapred.RecordReader;
import org.apache.hadoop.mapred.InputSplit;
import org.apache.hadoop.mapred.TaskAttemptContext;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.JobContext;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.GenericOptionsParser;



public class ReverseIndexer {


/*    public class LinesInputFormat extends TextInputFormat {
         @Override
         public RecordReader<LongWritable, Text> createRecordReader(InputSplit split, TaskAttemptContext context) {
             return new LinesRecordReader();
         }

         @Override
         protected boolean isSplitable(JobContext context, Path filename) {
             // we have to make the file unsplittable since
             // we need to be able to count line numbers
             return false;
         }
    }*/
/*
    public class LinesRecordReader extends RecordReader<LongWritable, Text> {
         private LongWritable key;
         private Text value = new Text();
         private long start = 0;
         private long end = 0;
         private long pos = 0;
         private int maxLineLength;

         @Override
         public void close() throws IOException {
             if (in != null) {
                 in.close();
             }
         }

         @Override
         public LongWritable getCurrentKey() throws IOException, InterruptedException {
             return key;
         }

         @Override
         public Text getCurrentValue() throws IOException, InterruptedException {
              return value;
         }


    }*/

    public static class IndexerMapper
            extends Mapper<LongWritable, Text, Text, Text>{

        private Text word = new Text();

        public void map(LongWritable key, Text value, Context context
        ) throws IOException, InterruptedException {
            StringTokenizer itr = new StringTokenizer(value.toString());
            while (itr.hasMoreTokens()) {
                word.set(itr.nextToken().toUpperCase().replaceAll("[^A-Z]", ""));
                context.write(word, new Text(key.toString()));
            }
        }
    }

    public static class IndexerReducer
            extends Reducer<Text,Text,Text,Text> {

        private Text out = new Text();
        public void reduce(Text key, Iterable<Text> values,
                           Context context
        ) throws IOException, InterruptedException {
            String lines = "";
            for (Text val : values) {
                lines += val.toString()+" ";
            }
            out.set(lines);
            context.write(key, out);
        }
    }


    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        String[] otherArgs = new GenericOptionsParser(conf, args).getRemainingArgs();
        if (otherArgs.length != 2) {
            System.err.println("Usage: ReverseIndexer <in> <out>");
            System.exit(2);
        }
        Job job = new Job(conf, "reverse indexer");
        job.setJarByClass(ReverseIndexer.class);
        job.setMapperClass(IndexerMapper.class);
        job.setReducerClass(IndexerReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);
        FileInputFormat.addInputPath(job, new Path(otherArgs[0]));
        FileOutputFormat.setOutputPath(job, new Path(otherArgs[1]));
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
