# 🧑‍💻 Computer Engineering Fields
We can roughly divide computer engineering, as taught in the department at Cairo university, into software engineering, machine learning & AI, embedded systems and digital design (hardware), cyber security and networks.

The following is a breakdown of what each of these involve:

| Field | Working Areas |
| --- | --- |
| Software Engineering | Web, Mobile, Desktop App Development, DevOps, Testing, Game Development, Operating Systems |
| Machine Learning & AI | Data Science, Classical Machine Learning, Deep Learning (Research + Math) |
| Embedded Systems & Digital Design | Arduino, ARM, etc. for embedded systems and VHDL, Verilog, etc. for digital design |
| Cyber Security & Networks | Security and Networking Protocols and Algorithms |


The rest of this article will be devoted to explaining what each of these is about.

## Software Engineering

One definition for software engineering is "the process of developing, testing and deploying computer applications to solve real-world problems by adhering to a set of engineering principles and best practices". Thus, it is about:

### 🛠️ Development
Developing software is another way for saying writing code. Any software you interact with such as websites, mobile apps, computer programs corresponds to a text file containing code that make the software look, behave and function in the way that it does. Even your operating system (e.g., Windows) corresponds to text files with code.

Different programming languages are suitable for different types of software:

| Platform          | Example Programming Language     |
|-------------------|---------------------------------|
| Website  Interface | HTML, CSS, JavaScript    |
| Website  Logic | JavaScript, Python, Ruby, PHP, etc.    |
| Android Apps      | Java, Kotlin, JavaScript                     |
| iOS Apps          | Swift, Objective-C, JavaScript               |
| Windows Apps      | C#, C++, JavaScript                          |
| MacOS Apps        | Swift, Objective-C, JavaScript               |
| Windows itself   | C, C++, C#, Assembly                      |
| MacOS itself     | Objective-C, C, Assembly                |
| 3D Games     | Unity and C# or Unreal with C++                |

Thus, front-end web developers will have reasonable expertise in HTML, CSS, JS and back-end developers will have expertise in one or more of JavaScript, Python, Ruby, etc. Although JavaScript is all over the map, it is not always the best choice and there are variations on it (frameworks) for each different platform.

### 🧪 Testing
As the definition suggests, the next type of software engineering job is testing. Before software (of any of the types above) is rolled out to production (e.g., before the website goes live), extensive testing has to take place. Testers write code (test scripts) that automatically tests the software and report the results to software developers. Note that software developers also write small tests, but the serious work is carried out by software testers. Quality Assurance of QA is a broader concept that includes software testing.
![image](https://i.gifer.com/66Uj.gif)

### 🚀 Deployment
Deployment is the process of taking software from a development environment to a production environment (rolling out to production). When developers build a software (e.g., website), it is only available on the computers where it was coded. Deployment is how it gets to the end users. The DevOps field involves deployment which is a big topic, and other automation activities.

**You will cover about 10 courses in software engineering, 4 of which will be around programming and computer science fundamentals.**

## Machine Learning and AI

One well-established definition of AI is that it is "The ability of a computer to perform tasks commonly associated with intelligent beings." On the other hand, machine learning is one branch of AI where computer programs that learn from data are developed. Some programs, such as search algorithms, that can help a robot solve a maze, are called artificial intelligence but not machine learning because the program did not learn anything from data.

### 🤖 Machine Learning
Machine learning is about having some data and then using it to learn something interesting. The following table shows examples of data available and what can be learned from it.

| Example Dataset   | What Can be Learnt     |
|-------------------|---------------------------------|
Temperatures for a city in the past 10 years | Model that predicts the temperature for any next 10 days in the next year |
Supermarket Customer Purchase Data | Model that can predict what item X the customer will most likely buy if they already bought item Y |
A Collection of Faces with the Name of each Face | A model given a new picture of any face predicts the name correctly
| Historical Stock Prices                 | Model that predicts the stock price of a company in the next trading day. |
| Sentiment-labeled Movie Reviews         | A model that predicts whether a new movie review is positive or negative. |
Text by Humans and Conversations | A model that predicts what to say when a human says something (e.g., ChatGPT) |

In all cases, (i) the dataset is encoded into numbers and (ii) a mathematical model (function with unknown parameters) is optimized over the data to (iii) result in a function that can predict the target variable that was in the data (e.g., temperature) even if given data it has never seen before. Finding the best setting for the unknown parameters of the function by optimization or similar is called training the machine learning model. When people say that ChatGPT has 130B parameters it means that the function used for the mathematical model had 130B unknown parameters before optimization (which sets those parameters).

From this we conclude that machine learning heavily relies on mathematics and it is the main paradigm used to achieve artificial intelligence. Code is written to represent the mathematical model, train it and use it for prediction. Machine learning treats the computer as a calculator that can compute the function in the mathematical model. Despite the heavy reliance on mathematics, experimentation and serious decision making are also included in the process. 

Machine and deep learning libraries allow developers to focus on experimentation and decision making without worrying much about mathematics; however, knowing the mathematics can be important for both of these.

![image50](https://i.redd.it/tscfed1aulw51.jpg)

### 🧠 Deep Learning
A branch of machine learning that uses deep neural networks which are just a specific form for the mathematical model. It is deep because the function is highly composite (function inside function inside function...) and it can be represented graphically by a network. Deep learning is much better than other machine learning approaches when the data is unstructured (e.g., images, videos, audio, text and not just an Excel table), which have more staggering application.

**You will cover about 9 courses in AI & Machine Learning. About 3-4 will involve deep learning.**

Python is the programming language most commonly used for this field.

## Embedded Systems and Digital Design

These are the two hardware-related fields that you will be introduced to in the department. They are very different from one another.

### 🕹️ Embedded Systems

An embedded system is defined as "a computer system (has similar but often simpler components than computer) that has a dedicated function within a larger mechanical or electronic system." The larger system where the computer system is embedded is most likely a robot or a device that is used in a specific industry.

With embedded systems, one can build a robot that solves a maze or makes dance moves or anything specific when blended with AI it can result in self-driving cars or tourist guide robots. Other specific basic examples include washing machines, air conditioners, kettles and etc.

The way embedded systems are achieved is by programming the computer system (writing code) so that is controls the other peripherals on the larger system (e.g., motors or actuators) to achieve the desired behavior. With this, a washing machine can be programmed by writing code so that the computer system starts a specific motor when a specific input is given or a robot can be programmed by making its motors and actuators move in a specific direction and angle based on sensor input.

![image](https://images.axios.com/vFO6a3A0uWsSgSpFL2dDugBixSY=/2018/10/16/1539653097522.gif)

C is one of the most common programming languages used for embedded systems.

### 🖱️ Digital Design

Digital design is about designing and building digital devices which include processors, graphical processing units and other digital computer units that can be part of the computer. It is achieved by hardware description languages such as Verilog and VHDL that are used to describe the hardware with code, the code is then converted to actual hardware by a fabrication lab.

**You will cover about 7 courses on hardware. 3 related to fundamentals, 2 related to embedded systems and 2 related to digital design.**


## 🌐🔒 Cyber Security and Networks

This involves writing code so that different devices can communicate with each other. Because the signals are sent over cables or over air, security becomes a serious issue so code is also written to help with security. 

**You will cover about 1 course on cyber security from a theoretical point of view and 1 course on networks.**