# Soteria
Soteria is the Greek godess of safety and refuge. We built Soteria, an patient-centric telehealth platform for refugees, for TreeHacks 2020. We won Stanford McCoy Family Center for Ethics in Society's $2000 prize for the Most Ethically Engaged Hack, and AlwaysAI's prize for the best application of Computer Vision for Medical Access.

### We consider ethical technology development an important responsibility for all engineers. 
### Read on to see our ethical analysis!

## Inspiration
One of our hackers spent over *1500 hours* working with refugees fleeing Syria, Afghanistan, and South Sudan. She found that many of these refugees had plenty of health issues, but also plenty of (justified) fear of authority figures, preventing them from seeking out medical care. These refugees will **delay treatment** because they are scared of having their identities exposed.

Global refugee crises have critical implications to a country’s economic, political and social development. During their migration, the refugees are often in dire need of medical care, but realize that it is too costly and too risky to seek such professional help. They are scared that if they go to a doctor in a country they pass by before they enter their destination country, they will never be granted legal asylum status there. They also lack the paperwork that reflects their medical history and provides them with medical care. As a result, in European countries like Germany and Belgium where healthcare is free for all citizens, refugees suffer from a lack of safe and low cost medical care that creates social inequality.

Soteria aims to strike a delicate balance -- between providing caregivers important information about each patient, crucial for accurate diagnoses, while maintaining patient privacy such that individuals can seek medical help confidently *without fear of retribution.* 

## What it does
As migratory pressure becomes increasing strenuous on overburdened healthcare systems, legislative, administrative, and financial barriers drastically reduce individual access to medical care. Issues range from lack of reliable information on the illness to cultural barriers, lack of knowledge of available services, and failure of administrative coordination. 

Named after the Greek goddess of salvation, Soteria is a telemedicine platform that connects refugees with confidential, low cost, high quality medical care. Our intent is to make healthcare accessible for populations in transit in all kinds of scenarios--from routine health check ups of day to day life in a new country to the organized chaos of a newly established refugee camp. 

We envision our product applied in two primary verticals: emergency medicine, and daily usage. In large scale public health emergencies, we see our product having the potential to minimize risk and exposure for healthcare workers in the diagnosis and triage of large populations, in both minimizing workload through our automated classifiers and minimizing exposure to harmful pathogens. In day to day usage, we see our low-cost telemedicine solution as an alternative to a doctor’s office, allowing vulnerable populations to access the care they need without the financial and legislative barriers originally in place.

With that in mind, the Soteria device is designed to be light weight, compact, and mobile to allow for usage in dynamic, rapidly changing environments closely tied with the mobile nature of refugee populations. Government and non-governmental organizations (e.g. MSF) are capable of providing rapid and highly specialized care without the expenses of ground deployment of specialists or the risk of contracting rare infectious diseases, while still allowing doctors to perform their diagnoses effectively given the remote collection of basic classifiers.

Soteria’s core platform consists of a camera and a heart rate sensor, attached to a raspberry pi. When a patient uses the device, Soteria is designed to automatically recognize the age, gender, and basic classifiers of the patient to expedite the triage process, particularly for individuals that generally lack detailed healthcare records due to the nature of their status. Automating the collection of basic identifiers allows us to categorize and triage patients on a far greater scale, in the vein of expanding low cost affordable healthcare for marginalized, vulnerable patients without access to healthcare.

## How we built it
We had three major components to our hack: The hardware, backend/ML, and the frontend.

### Hardware

We used a Tragoods Heart Rate Monitor, wrote low-level c++ code to interface with it on a Arduino Uno, and sent the heart rate information on to a Raspberry Pi over serial. We also used a Raspberry Pi camera to collect video of each patient.

We 3D printed, over the course of 9 hours, a custom stand and diagnosis apparatus for holding the Raspberry Pi, power source, sensors, camera, and Intel Movidius NCS, together in the correct position.

### Machine Learning/Backend
We use **three** different neural networks in our hack - A face detector using SSD on a ResNet-10 backbone, an age detector using SSD on a MobileNetV2 backbone, and a gender detector using SSD on a MobileNetV2 backbone.

The age and gender recognition models were trained on the Adience Gender and Age Classification Benchmark, while the face detector was trained on the MSCOCO dataset. The face detector’s predictions were used to select faces for the gender and age detector to predict on. We then blur out faces by applying a Gaussian filter over all regions of the image containing a face.

The models were deployed to a Raspberry Pi 4 with a Intel Neural Compute Stick 2, and ran in **real time (10fps)**. 

### Frontend
We built a Flask webpage to demo our telehealth platform, using HTML and CSS with some jQuery. The page consists of three parts, the intro, mission, and demo of the product. The frontend is mostly static with the exception of the live video feed, which runs each frame through the AlwaysAI backend and dynamically updates the results.

## Challenges we ran into
1. Integrating low-level sensor libraries with python code across multiple edge devices and the development computer. 
2. Stitching together code from python, c, javascript, and using dozens of packages from all over.
3. Integration of heart rate sensor/arduino with raspberry pi.
4. 3D printing/Autocad structural design.
5. Getting sleep.

## Accomplishments that we're proud of
1. Getting 3 computer vision models to play well together on a raspberry pi for real-time inference. 
2. Understanding how to connect a raspberry pi camera and an arduino heart rate sensor into one product. 
3. Getting sleep.

## What we learned
1. How to stream video robustly with dynamic flask webpages.
2. How to build peer-to-peer communication
3. How to integrate across the whole stack, from hardware to machine learning.
4. Rapid prototyping.


## What's next for Soteria
Firstly, understanding the interplay between too much or too little information would immediately inform our ability to fulfill our mission of helping improve the lives of refugees. While it might seem interesting to load our platform with all kinds of sensors and monitors, it becomes impossible to retain our mission of low-cost accessible care. On the flipside, a bare-bone device with a minimal amount of sensors and data might compromise the ability of physicians to provide accurate, effective medical advice due to lack of information. As two sides of the same coin, these considerations are invariably intertwined: do you provide an abundance of information at risk of decreasing accessibility? Or do you prioritize accessibility at the risk of compromising your core service/value? These are questions we hope to better understand.

It would be worthwhile to investigate the intrinsic value of our basic classifiers to doctors, and understand some of the drawbacks to telemedicine that we can work to address. While we can imagine that the physical limitations means doctors might not be able to listen to your breathing through a stethoscope, it’s important to understand if there exists the ability to mirror that information/conclusion using another sensor or develop a similar understanding through other metrics. Understanding how doctors generally diagnose patient conditions, particularly in a telemedicine setting, would allow us to develop our product in a patient/doctor-centric manner and optimize our sensor array to maximize the amount of useful information while retaining financial accessibility.

A potential application we considered was the reduction of social stigmas in certain areas through the use of telemedicine; more specifically, it means that refugees might have access to doctors that spoke their language and understood their culture through our platform, conditions that may not exist in their region. Understanding how we could potentially tailor our platform for certain regions, cultural differences, ethnicities, etc. may be useful in optimizing for regions where political instability produces a significantly larger proportion of refugees, or targeting certain areas where refugee health outcomes are particularly poor. 

Building out a robust backend and productionizing our telehealth platform are the natural next steps towards building a useful product. 


## Ethics
We believe that access to healthcare is a basic human right, and that it is ethically wrong for us as a society to not act against the problem of the lack of medical care among refugees. And this is not a small problem. There were an estimated **70 million** refugees worldwide in 2018, who are afflicted with a bevy of chronic and acute health conditions, exacerbated by poor living conditions and lack of access to medical care.

When approaching this problem, we had the advantage of having a team member who had spent a lot of time working with refugees, who understood how they oriented themselves towards authority figures and medical care. Privacy was their largest concern - thus, privacy was our largest focus.

Continuing on with our patient-centered design process, we then turned to the ethical rule set by Edmund Pellegrino (Sulmasy, 2014).  He argues that there exist three main components to the doctor-patient relationship:
A patient who is sick and needs help
A doctor who feels responsible for helping the patient
Medical action/application of medical science

We believe that patients should voluntarily refer to doctors, which can only be done when he/she trusts that doctor. In order to eliminate barriers and to facilitate this development of trust, we hence blur the patient’s image in order to eliminate stereotypes within and amongst physicians and thereby believe we can even out the quality of care.

At the same time, we recognize the need for a patient’s respect for physician feedback and vice versa and acknowledge that the use of telemedicine makes this more difficult. Nonetheless, we believe that this low-cost, highly effective live video streaming surface could bring a large amount of benefit, and that as long as we prioritize the patient first, both in their health and in their freedom, we will be doing patients a favor rather than harming them.

However, it’s important to be thoughtful of some of the ethical pitfalls of our technology. There exist many ethical issues to further explore:

1. First, we must ensure that patient information security and confidentiality are of utmost importance, in regards to both immigration status and health status. Otherwise, any benefit we provide them could be more than offset by the damage we do to their identity. Thus, we must make sure we keep patient data 100% confidential when receiving, storing, and transferring data.
2. Secondly, we must consider that while this will increase access to healthcare for some, there will exist segments of the population that will continue to be deprived of even telemedicine services, due to either knowledge or financial gaps. This is true not just on an individual level but also on a country level, where high cost often deters them from investing in such technologies. Typically, it means that Western nations end up providing care for unstable regions in Africa, the Middle East, Asia, etc. We must recognize the inherent biases this presents--in healthcare providers being almost exclusively from Europe or North America--whether it’s through unconscious biases with which we view and treat refugee populations, or potential personal biases (eg. patronizing views for Syrian refugees) that physicians impose upon vulnerable populations throughout their treatment and care. 
3. Third, there is well known research (Bulamwini, 2018) that shows facial recognition with AI can be highly biased, and perform worse on minorities because the underlying training dataset might be skewed towards residents of first-world nations. We think this is a particularly large area of concern, as refugee populations often have a disproportionate number of ethnic minorities. Long-term strategies to address this bias include retraining our AI models on more diverse and representative datasets.
4. Ethical considerations must include a robust understanding of the issue from the public health perspective. Refugees, knowing their identities are protected, might contact doctors with a highly contagious disease, like coronavirus. It then becomes impossible for doctors to, firstly, make a conscious decision of whether or not to report this individual for suspicious symptoms given the competing elements of ‘the greater good’ and their Hippocratic Oath. *Even if* the doctor should choose to prioritize public health, the built in privacy features of our product may mean that they then lack the means to effectively report the suspected patient due to lack of specific identifiers, and a built-in tracking option for public health emergencies would thereby undermine the patient-centric vision of our product. In future development, it becomes crucial for us to understand and delineate between acceptable and unacceptable situations; while patient privacy remains at the center of our focus, when and if authorities should be allowed to unblur or identify the patient they are speaking to.
5. In addition, we have to understand how our service might be integrated or made available in various social and political contexts. In certain states where censorship is particularly prevalent, complex political environments introduce an additional element for concern. Perhaps our platform could be utilized by certain politically-motivated groups for the spread of information (or disinformation). For example, political groups in rural India, with access to these refugees who could one day become formal citizens with voting powers, might be influenced in a tremendous capacity by the information they receive from an authoritative medical figure given a lack of other sources of media and information. In certain countries such as China, it may be impossible for MSF to provide telemedicine services to refugees due to the inability of the government to regulate the information and topics of conversation that emerge on air; state monitoring of our services would then compromise our promise of privacy and anonymity. It’s incredibly important, in the development of our platform, to understand the complex and multifaceted social/political environments (noting the significant correlation between social/political instability and refugee populations) in which our product might be applied, and perhaps tailor different adaptations or versions of our product for specific scenarios.

A good tangible next step in addition to the ideas mentioned above would be to design a proper patient consent form that both supports patients’ ethical rights and removes any concern about confidentiality of the data. Our goal is to provide a safe space for refugees to seek medical access and thus should be as transparent as possible. We ardently hope that Soteria is the first step towards a healthier future for displaced peoples around the globe.


## Bibliography 
Buolamwini, Joy, and Timnit Gebru. "Gender shades: Intersectional accuracy disparities in commercial gender classification." Conference on fairness, accountability and transparency. 2018

Sulmasy, Daniel P. "Edmund Pellegrino's philosophy and ethics of medicine: an overview." Kennedy Institute of Ethics Journal 24.2 (2014): 105-112
