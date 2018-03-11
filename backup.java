/*Citations https://www.youtube.com/watch?v=_xIWkCJZCu0
* March 10 2018*/


package com.example.syn_tax;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.Environment;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.InputStream;

public class AddTaskActivity extends AppCompatActivity{
    //private so only this class knows o f the id final cause its gonna remain the same
    private static final int RESULT_GET_IMAGE = 1;
    ImageView viewImage;
    Button addPhoto;



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_add_task);

        //get a reference to the image
        ImageView viewImage = (ImageView) findViewById(R.id.imagePhoto);

        //get a reference to the texts
        EditText edittitle = (EditText) findViewById(R.id.titleText);
        EditText editdesc = (EditText) findViewById(R.id.descriptionText);
        TextView status = (TextView)findViewById(R.id.status);


        //get user input
        String title = ((EditText) findViewById(R.id.titleText)).getText().toString().trim();
        String desc = ((EditText) findViewById(R.id.descriptionText)).getText().toString().trim();

        if (title.isEmpty())
            return;

        if (desc.isEmpty())
            return;

        //adding user input to out list
        //arrayAdaptertodo.add(title);
        //clearing title
        edittitle.setText("");
        editdesc.setText("");

    }


    //clicking the location button brings user to the location
    public void addLocation(View view) {
        Button location = (Button) findViewById(R.id.locationBtn);
        Intent location1 = new Intent(getApplicationContext(),LocationActivity.class);
        startActivity(location1);
    }


    //clicking the add task button brings user back to the homepage
    public void addTask(View view) {
        Button addtask = (Button) findViewById(R.id.addTaskBtn);
        Intent addtasks = new Intent(getApplicationContext(),HomeActivity.class);
        startActivity(addtasks);
    }


    //invoke gallery when user clicks
    public void addPhoto(View view) {
        Button addPhoto = (Button) findViewById(R.id.addPhoto);

       //invoke image gallery using an implicit intent
        Intent galleryIntent = new Intent(Intent.ACTION_PICK);

        //where do we want to find this data
        File photoDirectory = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_PICTURES);
        String photoDirect = photoDirectory.getPath();

        //finally get the Uri rep
        Uri data = Uri.parse(photoDirect);

        //set the data and type(get all image types)
        galleryIntent.setDataAndType(data,"image/*");

        startActivityForResult(galleryIntent, RESULT_GET_IMAGE);
    }


    //method called when user has selected a picture from the gallery
    //here we set the image the user has uploaded
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        //make sure the gallery intent actually called our method
        //Make sure the result was okay
        //Make sure that we actually have an image
        if(requestCode == RESULT_GET_IMAGE && resultCode == RESULT_OK && data != null) {
            //uniform resource indicator - shows us the address of the image tha has been selected
            Uri imageUri = data.getData();
            viewImage.setImageURI(imageUri);

            //declare a stream tor read the image from the sd card
            InputStream inputStream;


            //we get an input stream based on the uri of the image
            try {
                inputStream = getContentResolver().openInputStream(imageUri);
                //getting a bitmap from the stream
               Bitmap photo =  BitmapFactory.decodeStream(inputStream);
               //show image to our user
               viewImage.setImageBitmap(photo);

            }catch (FileNotFoundException e) {
                e.printStackTrace();
                Toast.makeText(this,"Unable to open image",Toast.LENGTH_LONG);
            }
        }
    }
}



