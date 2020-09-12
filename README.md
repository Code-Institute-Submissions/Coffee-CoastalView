# Coffee & Coastal Views 
[Coffee & Coastal Views](https://coffee-coastal-view.herokuapp.com/) is a web application that contains information about cafes along the Wild Atlantic Way in Ireland. It is a website that allows users to find cafes serving quality coffee in popular tourist locations. Site visitors can browse cafe reviews and ratings or they can make an account and leave their own reviews/rate the cafes. Users can also add cafes to their collection of "want to visit" for easy recall when they are in the area.

Users will also have the ability to, once registered and logged in, edit and delete the reviews and rating they have left previously.

The aims of the site is to create awareness for cafes serving quality coffee along Ireland's coast. 

Users will be able to perform CRUD (Create, Read, Update and Delete) functions across the site. 

Site visitors will also be allowed to fill out a form if they would like a new cafe added to the site. The site will then be added by admin. 



#  UX
The website was designed with registered users at the fore-front of the design.

-   As a user of the site I want to be able to register.
-	As a  registered user I want to be able to Navigate to different pages of the website 
-	As a  registered user I want to be able to click on a coffee shops and be brought to their website or social media 
-	As a  registered user I want to rate Coffee shops on the website and add my personal review 
-	As a  registered user of the website I want to be able to search for a coffee shop by location 
-	As a  registered website user, I want to be able to add, update and delete reviews.
-	As a  registered website user, I want to be able to add cafes to my "favourites/want to list list"
-	As a registered website user, I want to be able to remove cafes from my “favourites/want to visit” list. 

# Mock Ups
I designed the mock ups for the site using Figma. Mock ups for the website can be found in the following [folder](/MockUps)

#  Database Design
Before beginning my project I used [Draw.io](https://www.draw.io/) to create the Database Schema and flowcharts of many of the main use cases.
which helped me to visualize how the project would work and how the code should be written. Please find the Schema & flowcharts files in the following [folder](/DatabaseDesign)

# Technologies Used
* [HTML](https://html.com/) – the project uses html as the main language to build the website
* [Materalize](https://materializecss.com/) – Used as the main frontend framework.
* [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS) – CSS is used to add individual style to the website
* [Javascript](https://www.javascript.com/) - JS was used to initate certain features of Materalize.
* [Font Awesome](https://fontawesome.com/) – this site was used to add icons to the site.
* [MongoBD](https://www.mongodb.com/cloud/atlas/register) - Used as the main database technology.
* [Jinga](https://jinja.palletsprojects.com/en/2.11.x/) - Used as the main templating language for template manipulation.
* [Heroku](https://signup.heroku.com/?c=70130000000NeLCAA0&gclid=Cj0KCQjw-uH6BRDQARIsAI3I-UcV96h-n1NbhCxrdQnrMSjNQ72hwiisldeoifqoNJDw0Bf6ekDhtvwaAq5iEALw_wcB) - Used to host the website.

#  Important Features
## NavBar
This feature allows user to move from page to page. When a user is logged in it displays an option to visit a page called "Profile" which is the users profile page. There is also a link to "Logout" if a user is logged in. In the case that no user is logged in the NavBar simply displays a "Login" Tab.
##  Search Box
This allows logged in users to search for a cafe by typing in part of the name (it ignores glue words such as "the" or "and") or the location of a cafe. A new page loads with the search findings, unless there are no matches in which case a page renders that displays a "No search results" message. 
## Forms
A number of forms are used throughout the website. These forms allow users to register, sign in, submit reviews and request new cafes to be added to the website. 
## Modals
The website makes use of modals to ensure that users are sure they want to delete a review or favourite. 
## Flash Messages
Flash messaging is used throughout the site to inform users when an action has been completed. E.g "you have now logged out" 
## Email
I created a test email on gmail and the app uses this to create responses to users who request a cafe to be added to the website.

# Features left to implement:
1. Pagination - In the future I would like to add the Pagination feautre to display cafes and reviews in a tidier manor. 
2. Admin Page - I would also like to add a admin page where an admin user could login and have different functionailty to a normal user. Such functionailties could include adding a new cafe. 

# Deployment
I used Visual Studio to write, test and run my code before merging this code onto Gitpod for the purpose of this project.
On completion of each section I committed the work to GitHub. From the Github platform, I deployed the project to a hosting platform. The project is hosted on [Heroku](https://www.heroku.com/); in order to make the project go live, I had to insure I had the correct settings employed in Gitpod/Heroku. I used git in the command line and followed the instructions supplied by Heroku. Once activated my site was available at the following address: (https://coffee-coastal-view.herokuapp.com/).
## Deployment Security
I used the Heroku configuration variables option to configure sensitive data such as email credentials, secret keys, admin users and passwords. 

# Testing and Debugging
- Python:  I used the built-in Python dedugger in Visual Studio to debug my Python. I set breakpoints to see where certain functions/code was failing. This was a really useful tool throughout the development of this project. I also used [ExtendClass.com](https://extendsclass.com/python-tester.html) to validate my python code. No syntax errors were detected.
- HTML & CSS: In order to validate my HTML & CSS I availed of [W3C Validator](https://jigsaw.w3.org/css-validator/validator) which returned no errors.
- Javascript: I used [Esprima](https://esprima.org/demo/validate.html) to validate my javascript and no errors were returned. I used the console on chrome to help debug my Javascript code.
- Responsive: To test if the website was responsive I used the following [website](http://ami.responsivedesign.is/#) - the website was responsive across all screen sizes. 
- Python Logger: I also used the python logger app to help debug my python code.
- [RoBo 3t](https://robomongo.org/): This was a very helpful tool to anayalze the Mongo collections and queries. 

# Additional Resources
In order to complete this project I studied MongoBD in great depth and complied some useful functions and resources that I found very 
beneficial. I complied them in a wiki which can be viewed [here](https://github.com/Jadeosull93/Coffee-CoastalView/wiki).

# Credits
## Contents 
All imagery and addresses were taking from [Instagram](www.Instagram.com) and are to be used for the purpose of this project only. 

##  References 
All links can be found in my [Github Wiki](https://github.com/Jadeosull93/Coffee-CoastalView/wiki)

## People
A special thank you to my father John who has shown great patience in explaining certain concepts and investing his spare time into helping me to understand and unravil issues I encountered through the process. 
Another Thank You to my mentor [Precious Ijege](https://github.com/precious-ijege/) who has been incredibly patient throughout this project as I had started a new job and was struggling. He has given excellent constructive feedback as always and pushed me to develop the project to the best of my abilites. 
