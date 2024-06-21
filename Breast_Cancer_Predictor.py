import tkinter as tk
from tkinter import messagebox
from tkinter import Spinbox, OptionMenu, StringVar
import joblib
import pandas as pd

# Load the model
model = joblib.load('breast_cancer_model.pkl')

# Function to predict
def predict():
    try:
        # Collect the input data from the user
        data = {
            'Age': int(entries["Age"].get()),
            'Menopause': menopause_option.get(),
            'Tumor Size (cm)': int(entries["Tumor Size (cm)"].get()),
            'Inv-Nodes': inv_nodes_option.get(),
            'Metastasis': metastasis_option.get(),
            'History': history_option.get(),
            'Breast': breast_option.get(),
            'Breast Quadrant': bq_option.get()
        }
        
        # Create DataFrame
        input_data = pd.DataFrame([data])
        
        # Encode categorical data
        input_data['Menopause'] = input_data['Menopause'].map({'True': 1, 'False': 0})
        input_data['Inv-Nodes'] = input_data['Inv-Nodes'].map({'True': 1, 'False': 0})
        input_data['Metastasis'] = input_data['Metastasis'].map({'True': 1, 'False': 0})
        input_data['History'] = input_data['History'].map({'True': 1, 'False': 0})
        input_data['B_Left'] = input_data['Breast'].map({'Left': 1, 'Right': 0})
        
        # Breast Quadrant encoding
        quadrants = ['Lower inner', 'Lower outer', 'Upper inner']
        for quad in quadrants:
            input_data[f'BQ_{quad}'] = (input_data['Breast Quadrant'] == quad).astype(int)
        
        # Drop the original 'Breast' and 'Breast Quadrant' columns
        input_data.drop(columns=['Breast', 'Breast Quadrant'], inplace=True)
        
        print(input_data)

        # Predict
        prediction = model.predict(input_data)
        result = "Benign" if prediction[0] == 1 else "Malignant"
        
        # Display result
        messagebox.showinfo("Prediction Result", f"The prediction is: {result}")

    except Exception as e:
        messagebox.showerror("Error", f"Error occurred: {str(e)}")
        
# Create the main application window
app = tk.Tk()
app.title("Breast Cancer Prediction")

entries = {}

options_tf = ["True", "False"]
options_breast = ["Left", "Right"]
options_bq = ["Upper inner", "Upper outer", "Lower inner", "Lower outer"]

# Create and arrange the widgets
tk.Label(app, text="Age").grid(row=1, column=0, padx=10, pady=5)
entries["Age"] = tk.Spinbox(app, from_=1, to=100)
entries["Age"].grid(row=1, column=1, padx=10, pady=5)

menopause_option = StringVar(app)
menopause_option.set("Select an Option")
tk.Label(app, text="Menopause").grid(row=2, column=0, padx=10, pady=5)
OptionMenu(app, menopause_option, *options_tf).grid(row=2, column=1, padx=10, pady=5)

tk.Label(app, text="Tumor Size (cm)").grid(row=3, column=0, padx=10, pady=5)
entries["Tumor Size (cm)"] = tk.Spinbox(app, from_=1, to=20)
entries["Tumor Size (cm)"].grid(row=3, column=1, padx=10, pady=5)

inv_nodes_option = StringVar(app)
inv_nodes_option.set("Select an Option")
tk.Label(app, text="Inv-Nodes").grid(row=4, column=0, padx=10, pady=5)
OptionMenu(app, inv_nodes_option, *options_tf).grid(row=4, column=1, padx=10, pady=5)

metastasis_option = StringVar(app)
metastasis_option.set("Select an Option")
tk.Label(app, text="Metastasis").grid(row=5, column=0, padx=10, pady=5)
OptionMenu(app, metastasis_option, *options_tf).grid(row=5, column=1, padx=10, pady=5)

history_option = StringVar(app)
history_option.set("Select an Option")
tk.Label(app, text="History").grid(row=6, column=0, padx=10, pady=5)
OptionMenu(app, history_option, *options_tf).grid(row=6, column=1, padx=10, pady=5)

breast_option = StringVar(app)
breast_option.set("Select an Option")
tk.Label(app, text="Breast").grid(row=7, column=0, padx=10, pady=5)
OptionMenu(app, breast_option, *options_breast).grid(row=7, column=1, padx=10, pady=5)

bq_option = StringVar(app)
bq_option.set("Select an Option")
tk.Label(app, text="Breast Quadrant").grid(row=8, column=0, padx=10, pady=5)
OptionMenu(app, bq_option, *options_bq).grid(row=8, column=1, padx=10, pady=5)

# Add the predict button
predict_button = tk.Button(app, text="Predict", command=predict)
predict_button.grid(row=10, columnspan=2, pady=10)

# Run the application
app.mainloop()
