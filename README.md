# ATS
ATS Resume Analyzer is a Streamlit-based AI application that performs OCR-driven resume parsing and ATS-style evaluation. The system converts PDF resumes into text using Poppler and Tesseract OCR, then analyzes the extracted content against a provided job description using Google Gemini 1.5 Flash. It generates structured insights including resume strengths, weaknesses, missing keywords, and an estimated ATS match percentage, enabling automated, data-driven resume screening.

The following is the workflow/pipeline of the project:

[ User ]
   |
   v
[ Streamlit UI ]
   |
   v
[ PDF Upload ]
   |
   v
[ Poppler ]
(PDF → Images)
   |
   v
[ Tesseract OCR ]
(Images → Text)
   |
   v
[ Text Preprocessing ]
   |
   v
[ Gemini 1.5 Flash ]
(NLP + ATS Logic)
   |
   v
[ ATS Insights ]
   |
   v
[ Streamlit Output ]

