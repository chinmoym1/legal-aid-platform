#affdavit_template.py

from jinja2 import Template

affidavit_template = """
AFFIDAVIT

STATE OF {{ state }} COUNTY OF {{ county }}

{{ name }}, being first duly sworn, hereby declares and affirms as follows:

I. Introduction

My name is {{ name }}.
I am a {{ nationality }}.
My address is {{ address }}.

II. Statement of Facts

{{ facts }}

III. Jurat

I do solemnly swear that the foregoing statements are true and correct to the best of my knowledge and belief.

IV. Signature

Signed on {{ date }} at {{ city }}, {{ state }} before me:

[Your Signature]

V. Notary Public's Information

My commission expires: {{ commission_expiry }};
I am a notary public for the State of {{ state }};
My notary public number is: {{ notary_number }}.

VI. Certificate of Acknowledgment

The foregoing instrument was acknowledged by {{ name }} on this day, {{ date }}, in my presence.

[Notary Public's Signature]
"""

data = {
    "state": "Delhi",
    "county": "New Delhi",
    "name": "Rahul Manchanda",
    "nationality": "citizen of India",
    "address": "123, Example Street, New Delhi",
    "facts": "- On 1st Jan 2025, I witnessed ...\n- Attached document is a true copy ...",
    "date": "30th August 2025",
    "city": "New Delhi",
    "commission_expiry": "31st Dec 2027",
    "notary_number": "NP-12345"
}

template = Template(affidavit_template)
print(template.render(data))
