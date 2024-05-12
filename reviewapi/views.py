from rest_framework.decorators import api_view
from django.http import JsonResponse
import fitz
import openai

openai.api_key = "sk-proj-nvshsPSlSwTO6TyFGm5vT3BlbkFJbMx154g5GZUyy4rAa6gd"


def extract_text_from_pdf(pdf_file):
    text = ""
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text


def review_resume(text):
    response = openai.completions.create(
        model="gpt-3.5-turbo-instruct", prompt=text, temperature=0.5, max_tokens=200
    )
    print(response.choices[0].text)
    return response.choices[0].text.strip()


@api_view(["POST"])
def resume_review(request):
    if request.method == "POST":
        if "resumeFile" not in request.FILES:
            return JsonResponse({"error": "No file part"})

        pdf_file = request.FILES["resumeFile"]
        if pdf_file.name == "":
            return JsonResponse({"error": "No selected file"})
        try:
            if pdf_file and pdf_file.name.endswith(".pdf"):
                resume_text = extract_text_from_pdf(pdf_file)
                # print(resume_text)
                review_text = f'''Suppose You are profession resume reviewer and I'm providing you the extracted texts from resume in double quotes and i want you to review this resume carefully and get me the proper review don't be biased towards positive review, anylyze the skillset, position, headline, Education and also the preivious experiences and projects and see whether it is align with the skill set and position give the review based on these criterias give me the reiview in just two point one should be 'Overall rating' which is out of 10 and second one should be 'Improvements' which is 3 points for improvements in brief,
                "{resume_text}"'''
                review = review_resume(review_text)
                saprated_text = review.split("\n")
                score = saprated_text[0].split("Overall Rating: ")[-1]
                points = saprated_text[1:]
                points = [i for i in points[1:5] if i not in ["\n", "Improvements:"]]
                return JsonResponse({"score": score, "points": points})
            else:
                return JsonResponse(
                    {"error": "Invalid file format. Only PDF files are supported."}
                )
        except:
            return JsonResponse({"error": "Internal Server Error"})
    else:
        return JsonResponse({"error": "Invalid Request"})
