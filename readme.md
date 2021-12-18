**TEACHABLE MACHINE RESTFUL IMAGE CLASSIFIER**
**Prerequisites:**

<p>Visit [ Teachable machine](https://teachablemachine.withgoogle.com/) for more.</p>

**Instructions**

> clone repo
> pipenv install
> python app.py

App will start running at http://hostname:5002
**TEST**
Using any http request lib, make a **POST** REQUEST TO **/api/v1/predictions**
FORM DATA >image (data type image )
**RESPONSE**
`json [ { "class": "person", "confidence": 0.9910551309585571 } ]`
