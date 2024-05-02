import streamlit as st
import pyrebase

# Firebase configuration
config = {
  "apiKey": "AIzaSyD--IxFhGdSr2FU3DlqSLYnTUTFkMTlDvE",
  "authDomain": "host-test-9bb6a.firebaseapp.com",
  "databaseURL": "https://host-test-9bb6a-default-rtdb.firebaseio.com",
  "projectId": "host-test-9bb6a",
  "storageBucket": "host-test-9bb6a.appspot.com",
  "messagingSenderId": "673454854896",
  "appId": "1:673454854896:web:e8ed1895586610e8c06835",
  "measurementId": "G-ZKYR6QPF92"
}

# Initialize Pyrebase
firebase = pyrebase.initialize_app(config)
db = firebase.database()

def query_firebase(exp_number, frame_number=None, class_filter=None):
    if frame_number:
        path = f"detections/{exp_number}/{frame_number}"
    else:
        path = f"detections/{exp_number}"
    
    results = db.child(path).get()
    all_entities = []

    if results.val() is not None:
        if frame_number:
            # Single frame data handling
            if "entities" in results.val():
                all_entities.extend(results.val()["entities"])
        else:
            # Handling multiple frames under the experiment
            for frame_data in results.each():
                if "entities" in frame_data.val():
                    all_entities.extend(frame_data.val()["entities"])

    # Filter by class if specified
    if class_filter is not None:
        all_entities = [e for e in all_entities if e["class"] == class_filter]

    return all_entities

def main():
    st.title("Query Realtime Database")
    
    with st.form("query_form"):
        exp_number = st.text_input("Experiment Number", value="exp1")
        frame_number = st.text_input("Frame Number (optional)", value="")
        class_filter = st.number_input("Class (optional, leave 0 to ignore)", value=0, min_value=0, format="%d")
        submit_button = st.form_submit_button("Query")
        
        if submit_button:
            if frame_number.isdigit():
                frame_number = int(frame_number)
            else:
                frame_number = None
            class_filter = None if class_filter == 0 else class_filter
            results = query_firebase(exp_number, frame_number, class_filter)
            if results:
                st.write("Results:")
                st.json(results)
                st.write(f"Number of hits: {len(results)}")
            else:
                st.write("No data found for the given criteria.")

if __name__ == "__main__":
    main()