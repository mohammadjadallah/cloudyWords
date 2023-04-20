# importing libraries
from flask import Flask, render_template, request
from wordcloud import WordCloud
import os

# Initialize the app
app = Flask(__name__)

# file to render
htmlf = "index.html"

def cloud_visualizer(
    text: str = None,
    background_color: str = "black",
    width: int = 500,
    height: int = 300,
    show: bool = False,
    saveimg: str = None,
    array: bool = False,
    specific_path: str = None
    ):
    """
    word cloud visualizer 
    -------------------------------------------------------------------------------
    text: the textual data used for visualizing the wordsm the type value is "str" by default equal to "None".
    
    background_color: to change the background color, by default equal to "black".
    
    width: to change the width of image the type value is "int" by default equal to "500".
    
    height: to change the width of image the type value is "int" by default equal to "300".  
    
    show: for sowing the image.
    
    saveimg: name of the file if None so the new image will not save.
    
    array: return the new image as an array.
    """
    
    # Initialize the WordCloud object
    wordCloud = WordCloud(collocations=False, background_color=background_color,
                         width=width, height=height)
    
    # Generate the image 
    gen = wordCloud.generate(text)
    
    if show:
        return gen.to_image()
    
    elif specific_path is not None and saveimg is not None:
        gen.to_file(specific_path + '\\' + saveimg + ".png")
        print(f'image saved in {specific_path}\\{saveimg + ".png"}...')
    
    elif saveimg is not None:
        gen.to_file(saveimg + ".png")
        print("New image is saved...")
        
    elif array:
        return gen.to_array()
    

text = ""

@app.route("/", methods=["GET", "POST"])
def render():
    global text

    if request.method == 'POST':
        # Retrieve the text from the textarea
        text = request.form.get('textbox', "")
        color = request.form.get("bgcolorSelector")
        # Print the text in terminal for verification
        # print(text)
        curdir = os.getcwd()
        if os.path.exists(f"{curdir}/static/outputs/output.png"):
            os.remove(f"{curdir}/static/outputs/output.png")
        try:
            cloud_visualizer(text=text, specific_path=f"{curdir}/static/outputs",
                    saveimg="output", background_color=f"#{color}")
        except:
            curdir = os.getcwd()
            if os.path.exists(f"{curdir}/static/outputs/output.png"):
                os.remove(f"{curdir}/static/outputs/output.png")
            

    return render_template('index.html', text=text)



if __name__ == '__main__':
    # Run the app
    app.run(debug=True)
