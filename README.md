# 🧁 CMP Docs

![image](https://i.imgur.com/YkpXfRH.png)

I was motiviated to to create an online platform that takes the form of software documentation as a guide for those that are considering enrolling, have enrolled or even have graduated form the department! After meeting with prospective students to help them decide whether or not to join the department and teaching a summer course to freshmen, I realized that a lot of questions are being repeatedly asked every year; it dawned on me that it would be really nice if answers to all such questions and more information about the computer engineering department at Cairo university are all available in one site.

You can check the documentation at [https://cmp-docs.netlify.app](https://cmp-docs.netlify.app)

**Thereby, the following are the motivations of this website:**

✦ Provide prospective students all the information they need to make an informed decision regarding 
whether or not to choose computer engineering

✦ Guide students that have just entered the department on how to cope and get ready for what's next. Some sections of the website will be even useful to graduate students!

✦ Realize the fact, that we are all one family; and that we are all ready to help one another no matter how far we are from each other.

## 🚆 Navigating the Website

> Beware, this effort is entirely controlled by us students. No professors are involved and this is not official in any sense.

It should be self-evident from the side bar; however, here is a small guide:

| Student Type         | Consideration                                   |
|----------------------|-------------------------------------------------|
| Prospective Students | Review the "Before Joining" section in the sidebar. If you have any unanswered questions, please create a GitHub issue. |
| Recent Students      | Consider the "Recently Joined" section.         |
| All Other Students   | Consider all mentioned sections and feel free to collaborate! |

**Important Note I**: The website is build to be updated continually; thus, checking it frequently for updates or changes is key.

**Important Note II**: The website is built with Arabic in mind. However, with this being initially written in English it may take some time until the Arabic versions of all pages are available. Collaboration here would be really helpful here.


## 🪂 We are all Contributors!

Despite being initiated by one student, the represenative of the senior class, Essam W. The website is built with collaboration in mind. In particular, as a student part of the department, you are welcome to change any part of the content found within the website with zero web development coding prerequisites. 

✦ Modifying any existing page takes only modifying its corresponding markdown or json file. A page in the documentation is represented by json (which supports markdown in strings) only if contains a grid; otherwise, it's pure markdown. This all gets transpiled to html and css under the hood.

✦ You can even modify the sidebar to include more sections and pages and guess what! The side bar is a single yaml file.

**Hint I:** it takes approximately 2, 3 minutes to learn the structure of each of json and yaml respectively and another 5 minutes for markdown. These are textual formats any experienced developer should be used to. 

**Hint II:** All files correpsonding to the website can be found inside "public/department". They follow the same hierarchy as the sidebar.

To run for the first time, install `Node.js` then type at the terminal
```
npm install
```
Now you can test any changes you perform by running
```
npm start
```

Once you're done. Simply submit a PR; it would be nice if you start proposing the PR as an issue if it's a big change.

#### Collaboration Notes

- Only write facts that you certainly sure of; otherwise, discuss in an issue first and demonstrate uncertianty in the text. Including sources or references or examples or natural deductions is required.

- Using gifs or emojis is highly recommended.

#### Known Issues

- Lists are not rendered properly in markdown. So far, manual bullets have been used.
- Likewise, Latex is not supported in markdown.

<h1 align="center"> Thank you 💗 </h1>
