import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from google import genai
from tkinter import font

# Initialize the Gemini client with your API key
client = genai.Client(api_key='API_KEY')

# Create global variables for the images to keep track of them
image1 = None
image2 = None

# Create the GUI window
root = tk.Tk()
root.title("Signature Verification System")
root.geometry("900x600")
root.configure(bg="#eaf0ef")

# Heading
title_label = tk.Label(root, text="Signature VERIFICATION SYSTEM", font=("Helvetica", 20, "bold"), bg="#eaf0ef", fg="navyblue")
title_label.pack(pady=20)


canvas1 = tk.Canvas(root, width=250, height=200, bg="#f8f9fa", bd=3, relief="ridge", highlightthickness=2, highlightbackground="#c2c2c2")
canvas1.place(x=100, y=110)

canvas2 = tk.Canvas(root, width=250, height=200, bg="#f8f9fa", bd=3, relief="ridge", highlightthickness=2, highlightbackground="#c2c2c2")
canvas2.place(x=500,y=110)

upload_icon = ImageTk.PhotoImage(Image.open("upload_icon.png").resize((60, 60)))
canvas1.create_image(125, 100, image=upload_icon)
canvas1.image = upload_icon

canvas2.create_image(125, 100, image=upload_icon)
canvas2.image = upload_icon

# Status Label
status_label = tk.Label(root, text="Status", font=("Arial", 14), bg="#eaf0ef")
status_label.place(x=400, y=340)

status_box = tk.Label(root, text="", font=("Arial", 12), width=30, height=2, bg="white", bd=2, relief="groove")
status_box.place(x=300, y=380)

# Verification Box
verification_box = tk.Label(root, text="", font=("Arial", 12, "bold"), width=27, height=2, bg="white", bd=2, relief="groove")
verification_box.place(x=300, y=480)


# Upload functions
def upload_image1():
    global image1, photo1
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", ".jpg;.jpeg;*.png")])
    if file_path:
        image1 = Image.open(file_path)
        img_resized = image1.resize((250, 200))
        photo1 = ImageTk.PhotoImage(img_resized)
        canvas1.create_image(0, 0, anchor=tk.NW, image=photo1)        
        canvas1.image = photo1
        upload_btn1.destroy()

def upload_image2():
    global image2, photo2
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", ".jpg;.jpeg;*.png")])
    if file_path:
        image2 = Image.open(file_path)
        img_resized = image2.resize((250, 200))
        photo2 = ImageTk.PhotoImage(img_resized)
        canvas2.create_image(0, 0, anchor=tk.NW, image=photo2)
        canvas2.image = photo2
        upload_btn2.destroy()

# Compare function
def compare_images():
    global image1, image2
    if image1 is None or image2 is None:
        messagebox.showerror("Error", "Please upload both signature images.")
        return

    prompt = "Compare these two signature images and determine if they are from the same individual. Only provide percentage, approximate nothing more any cases at worst case give any percentage nothing more"
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-preview-04-17",
            contents=[image1, image2, prompt]
        )

        comparison_percentage = float(response.text.strip('%'))
        status_box.config(text=f"Match Percentage: {comparison_percentage}%")

        if comparison_percentage > 95:
            status_box.config(bg="lightgreen")
            verification_box.config(text="Verified ✅ ", bg="lightgreen", fg="green")
        else:
            status_box.config(bg="tomato")
            verification_box.config(text="Not Verified ❌ ", bg="tomato", fg="red")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Buttons


upload_btn1 = tk.Button(canvas1, text="Upload First Image", command=upload_image1, bg="steelblue", fg="white", font=("Arial", 9))
canvas1.create_window(125, 170, window=upload_btn1)  # center of canvas

upload_btn2 = tk.Button(canvas2, text="Upload Second Image", command=upload_image2, bg="steelblue", fg="white", font=("Arial", 9))
canvas2.create_window(125, 170, window=upload_btn2)

match_btn = tk.Button(root, text="Verification Status", command=compare_images, width=15, bg="lightblue")
match_btn.place(x=380, y=440)


# Run the GUI
root.mainloop()
