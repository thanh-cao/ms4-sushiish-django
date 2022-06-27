# Suhiish - Testing
This section documents the testing phase of the Sushiish application covering reports from validators and tools testing, manual user stories testing, further functionality testing, known bugs and issues and what is left could be further improved. Return to main [README.md](README.md) to read more about project's planning, conceptions, technologies used, deployment.

## Table of contents
  - [During development](#during-development)
  - [Validators and tools](#validators-and-tools)
    - [W3C Markup Validation](#w3c-markup-validation)
    - [W3C CSS Validation](#w3c-css-validation)
    - [JSHint](#jshint)
    - [PEP8 Online](#pep8-online)
  - [User stories testing](#user-stories-testing)
  - [Further functionality and logic testing](#further-functionality-and-logic-testing)
  - [Further possible improvements](#further-possible-improvements)

## During development
* In the process of building front-end, Chrome DevTools was heavily utilized in order to make changes to markups and adjust layout responsively on multiple devices. Console tab was used intensively in order to debug and test JavaScripts functions and logic. Furthermore, various browsers (Google Chrome, Firefox, Safari, Internet Explorer) and physical devices (13-inch screen, 27-inch screen, iPhone X, Samsung Galaxy S9, iPad) were used to view the website in order to check the responsiveness.
* Python shell in terminal was used to print out variables and test functions.
* Manual testing different possible scenarios when developing a feature.

## Validators and tools
### W3C Markup Validation
* [W3C Markup Validation](https://validator.w3.org/) was used to validate the HTML codes of the website in all pages. There were only minor errors and warnings such as duplication of class, missing attributes in form fields, missing session heading, etc. They were all fixed accordingly to show no errors afterwards. Labels for form fields were added to make it more accessible.

### W3C CSS Validation
[W3C CSS Validator](https://jigsaw.w3.org/css-validator/) was used to check the CSS syntax. The results show no errors and warnings but the warnings are about prefixes for vendors as I have ran my css codes through a autoprefixer tool.

### JSHint
* [JSHint](https://jshint.com/) was used to check the JavaScript syntax. There were also minor warnings such as missing semicolons and missing variable declaration which were all fixed accordingly. There are still some warnings about unused variables and functions but it is because some of the variables are from Bootstrap (such as `scrollspy`, `bootstrap`), Stripe, or other javascript files.
  ![JSHint](readme-assets/testing/testing-productjs.png)
  ![JSHint](readme-assets/testing/testing-stripejs.png)

### PEP8 Online
* [PEP8 Online](https://pep8online.com/) was used to check the Python syntax. There were only warnings about line too long or indentation which were all fixed accordingly. The only warning left is on file `settings.py` file where there are still 4 lines too long at variable `AUTH_PASSWORD_VALIDATORS`. The longest line here is only 91 characters (which is 12 characters longer than the norm 79 characters). As this is system's related string and it doesn't affect the readability of the code, I have decided to leave them be.
  ![PEP8 Online](readme-assets/testing/testing-pep8.png)
  ![PEP8 Online](readme-assets/testing/testing-pep8-settingspy.png)

## User stories testing

## Further functionality and logic testing
1. Form validations:
* Intensive testing of form validations during development and after is done to ensure that all the fields are correctly validated and that the form is not submitted with invalid data.
* Required fields are filled out. Email and phone are submitted with correct format (email format and phone number should contain only 8 digits).
* If form is not validated, the form will not be submitted and the user will be notified with error texts or toast message.
* If form is validated, the form will be submitted and the user will be redirected accordingly or a success message shows up to inform of the success of form submission.
2. Navigation bar, buttons, and links: all the navigation links are working properly. Buttons should give users feedback when they are clicked. Links should go to where they should go and no broken links are present.
3. Responsiveness on different devices: application was thoroughly reviewed on different physical devices as well as Chrome DevTool.
4. Product filterings: category filters should show products within the chosen category. Allergy filters should show a list of products that don't include the chosen allergies. Search box should show products whose names or ingredients match the search term.
5. Correct data being shown to logged in user. User should be able to see/update/delete their own information and their order history, not other users'.
6. Restricted views: only superuser or admin users can access the restricted admin views. Profile view should only be accessible by its respective loggedin user.
7. Order flow and payment: the flow should be easy to understand and proceed with appropriate error feedback and so users could fix accordingly if they have any problems. Success payment should direct users to a success page and an email to confirm the order is successfully placed.
8. Stripe webhook handlers should be able to handle creating orders in database and/or create user profiles when payment is successful but there is a problem in the server or connection.
9. Create / edit / delete functionalities and routes work properly and reflected in changes in the database.
10. Admin dashboard should show all the available tables in the database and allow admins the possibility to create, edit, and delete data, except for read-only fields such as price-related fields in Order table.

## Further possible improvements
* Further refactoring could have been done to improve clean code and readability. This was done only to small extend due to the time constraint.