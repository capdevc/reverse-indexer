/**
 * Created by cc on 3/27/14.
 */

import java.io.IOException;
import java.io.DataInput;
import java.io.DataOutput;

import org.apache.hadoop.io.Writable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;


// class to hold information about a word occurence
public class LineRecWritable implements Writable {

    private Text filename;          // filename found in
    private IntWritable lineNum;    // line no found in
    private IntWritable position;   // position found at

    public LineRecWritable(){
        setFilename("");
        setLineNum(0);
        setPos(0);
    }

    public LineRecWritable(String filename, int lineNum, int position) {
        setFilename(filename);
        setLineNum(lineNum);
        setPos(position);
    }

    @Override
    public void readFields(DataInput in) throws IOException {
        filename.readFields(in);
        lineNum.readFields(in);
        position.readFields(in);
    }

    @Override
    public void write(DataOutput out) throws IOException {
        filename.write(out);
        lineNum.write(out);
        position.write(out);
    }

    public int getLineNum() {
        return lineNum.get();
    }

    public int getPos() {
        return position.get();
    }

    public String getFilename() {
        return filename.toString();
    }

    public void setLineNum(int lineNum) {
        this.lineNum = new IntWritable(lineNum);
    }

    public void setPos(int position) {
        this.position = new IntWritable(position);
    }

    public void setFilename(String filename) {
        this.filename = new Text(filename);
    }
}

