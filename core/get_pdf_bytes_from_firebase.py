import requests
def get_pdf_bytes_from_firebase(file_url):
    try:
        response = requests.get(file_url)
        response.raise_for_status()  
        file_bytes = response.content
        if len(file_bytes) > 4 and file_bytes[:4] != b'%PDF':
            raise ValueError("The downloaded file does not appear to be a valid PDF")
        return file_bytes
    
    except Exception as e:
        raise ValueError(f"Failed to download PDF via HTTP: {str(e)}")
# url1 = "https://firebasestorage.googleapis.com/v0/b/todo-a907b.firebasestorage.app/o/objectiveAnswerSheets%2F46hrpCCaeyGO9Lqkt732%2F1750973213531_CamScanner%2023-06-2025%2015.39.pdf?alt=media&token=389be867-b48c-4d51-aa1c-9b41c362dba7"
# url2 = "https://firebasestorage.googleapis.com/v0/b/todo-a907b.firebasestorage.app/o/objectiveAnswerSheets%2F46hrpCCaeyGO9Lqkt732%2F1750973200135_Taimoor%20Resume2.pdf?alt=media&token=c72fea37-17a3-46c1-aa01-42a2abf9399e"
# url3 = "https://firebasestorage.googleapis.com/v0/b/todo-a907b.firebasestorage.app/o/objectiveAnswerSheets%2Fsample_answer_sheet.pdf?alt=media&token=bc88e7c5-a3bc-4426-91bd-368753c5261a"
# # get_pdf_bytes_from_firebase(url)