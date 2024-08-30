import os
import time
import markdown
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv('API_KEY'))

video_file_name = "../static/videos/bench press.mp4"
print(f"Uploading file...")
video_file = genai.upload_file(path=video_file_name)
print(f"Completed upload: {video_file.uri}")

while video_file.state.name == "PROCESSING":
    print('.', end='')
    time.sleep(10)
    video_file = genai.get_file(video_file.name)

if video_file.state.name == "FAILED":
    raise ValueError(video_file.state.name)

prompt = """
As an expert fitness trainer, your task is to critically analyze gym videos, focusing on identifying and correcting improper exercise technique. I will specify the exercise being performed. Your analysis should be strict, with a low tolerance for form deviations. Follow these guidelines:

1. Evaluate the technique for the specified exercise, focusing on these critical aspects:
- Exercise form (highest priority)
- Proper body alignment and posture
- Range of motion and joint positioning
- Control and stability throughout the movement
- Proper breathing and muscle engagement

2. Present a comparison table of perfect form vs. observed form, something similar to this but for the specific exercise:

| Aspect            | Perfect Form                      | Observed Form                    |
|-------------------|-----------------------------------|----------------------------------|
| Depth             | Hips below parallel to ground     | Hips slightly above parallel     |
| Knee Alignment    | Knees track over toes throughout  | Slight knee caving on ascent     |
| Bar Path          | Perfectly vertical                | Slight forward lean at bottom    |
| Back Angle        | Consistent throughout movement    | Some rounding at bottom of squat |
| Breathing         | Brace and hold throughout rep     | Inconsistent breathing pattern   |

3. Rate the overall technique on a scale of 1 to 10, where:
0: Complete failure (e.g., barbell falls, unable to complete a single repetition)
1-3: Poor technique with multiple major form issues (high risk of injury)
4-5: Fair technique with several noticeable form issues
6-7: Good technique with a few minor form issues
8-9: Very good technique with only slight imperfections
10: Perfect technique (extremely rare, reserve for flawless execution only)

4. Provide a score breakdown explaining why it's not a perfect 10, detailing specific deviations from ideal form. For example:
"This is a 7/10 because:
- The depth of the squat is not quite to parallel (-1)
- There's slight knee caving on the ascent (-1)
- The bar path isn't perfectly vertical (-1)"

Remember:
- Even small form deviations should significantly impact the score.
- A score above 7 should be rare and given only for truly excellent form.
- Prioritize identifying potential injury risks and inefficiencies in the movement.
- Be direct and clear about problems - do not sugarcoat issues.
- Assume that improper form, if not corrected, will lead to injury or suboptimal results.

Your feedback must be constructive but critical, aimed at substantially improving the exerciser's technique and safety. The output should be in markdown format.
"""

model = genai.GenerativeModel(model_name="gemini-1.5-pro", system_instruction=prompt)

print("Making LLM inference request...")

exercise_name = "bench press"
response = model.generate_content([video_file, exercise_name],
                                  request_options={"timeout": 600})

print(markdown.markdown(response.text))

# List all files
for file in genai.list_files():
    print(f"{file.display_name}, URI: {file.uri}")
    # Delete file
    genai.delete_file(file.name)
    print(f'Deleted file {file.uri}')

# List all files
for file in genai.list_files():
    print(f"{file.display_name}, URI: {file.uri}")
