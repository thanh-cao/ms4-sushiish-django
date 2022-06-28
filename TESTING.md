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
### 1. As a new visitor and a site user, I want to...
  * ...know what the website is about upon landing the site.
    * When visitors land on the index page, they can see a hero text with a background image of a maki sushi which clearly indicate that this website is about sushi.
    * Landing page also has other sections which further give more context to the website such as catering service and introduction to Sushiish.
  ![Landing page](readme-assets/features/landing-hero-section.png)
  ![Landing page sections](readme-assets/features/landing-sections.png)

  * ...be able to navigate through the website smoothly.
    * The navigation bars, both on the index page and online shop section, are designed to be clear with texts, simple and focused, so that visitors can easily go to checkout and place an order with ease. The navigation bars are also responsive and adaptable to different screen sizes so that they don't suddenly expand and be obstructive to the screen property.
    ![Index navigation](readme-assets/features/index-nav-desktop.png)
*Index navigation desktop*
    ![Index navigation](readme-assets/features/index-nav-mobile.png)
*Index navigation mobile screen with hamburger dropdown*
    
  * ...be able to sign up / log in / log out in order to order take-away.
    * Sushiish utilizes `django-allAuth`, a tested and secured authentication system. The system is designed to be easy to use and easy to maintain, with a lot of features such as email verification, password reset, and more.
    ![Sign up](readme-assets/features/allAuth-signup.png)
    ![Sign in](readme-assets/features/allAuth-signin.png)
    ![Sign out](readme-assets/features/allAuth-signout.png)
  
  * ...have a personalized profile page where I can add my delivery information and see my previous purchase history.
    * User's profile page is only accessible by verified logged in user. The page contains a form to add/edit user's details, address information and a list of previous orders which belong to the respective user.
    ![Personalized profile page](readme-assets/features/profile-user.png)
    ![Profile page - saved address](readme-assets/features/profile-saved-addresses.png)
    ![Profile page - order history](readme-assets/features/profile-order-history.png)

### 2. As a shopper during the dish selection phase, I want to...
  * ...be able to see all the dishes available to buy and filter the dishes based on their categories.
    * Visitors can choose to see all the dishes available at Sushiish. Or they can choose to filter the menu by its category. The category is designed to be scrolled horizontally and is responsve to different screen size with arrow on mobile screen to indicate the user that there is more the sides. The category filter is also fixed upon scrolling so that users can just easily change category at any point.
    ![Dish categories](readme-assets/features/products-category-filter.png)

  * ...exclude the dishes based on certain allergies.
    * There are currently 10 allergies which are also some of the most common allergies. The user can choose to exclude the dishes which contain the allergies they are allergic to.
    ![Allergy filter](readme-assets/features/products-allergy-filter.png)

  * ...search for a dish based on name or descriptions (ingredients).
    * Visitors can search for a dish by its name or description (ingredients). The search box is also responsive and adaptable to different screen sizes.
    ![Search bar desktop](readme-assets/features/responsive-navbar-desktop.png)
*Desktop screen navbar with full search box*
    ![Search bar mobile](readme-assets/features/responsive-navbar-mobile.png)
*Mobile screen navbar with only search icon which hides/displays search box upon click*

  * ...view product's detailed information.
    * Detailed information of a dish can be found upon clicking the product card on product listing page. The details are displayed with an offcanvas on the right hand side of the screen. On dekstop, the offcanvas takes up a small portion of the screen while on mobile, it takes up the entire screen. Offcanvas can be closed by clicking outside of the canvas area or the close button.
    ![Offcanvas desktop](readme-assets/features/product-offcanvas-dekstop.png)
    ![Offcanvas mobile](readme-assets/features/product-offcanvas-mobile.png)
  
  * ...able to see the total amout of my current purchase at any time.
    * On the navigation bar, a cart icon is always visible with the total amount of the current purchase. Upon successfully added to cart, the total amount is dynamically updated and a toast message appears to inform buyers of the successful addition to cart.
    ![Navigation bar with cart](readme-assets/features/online-shop-nav-1.png)
    ![Toast success message add to](readme-assets/features/product-add-to-cart.png)

### 3. As a shopper during checking out phase, I want to...
  * ...view all the dishes I have added to my order.
    * Upon clicking cart icon on navigation page, buyer is directed to their current shopping cart where they have a complete overview of all the items that have been added to cart as well as the total amount of the current purchase and/or order discount/delivery charge.
    ![Shopping cart](readme-assets/features/cart-page.png)

  * ...easily adjust quantity of a product currently in my order / delete a product
    * For each item in the shopping cart, there is buttons where buyer can easily update the quantity of that specific item or delete it from the shopping cart. There is also a text button `Clear cart` at the bottom of all the order items, which will clear the entire shopping cart.
    ![Order item in shopping cart](readme-assets/features/cart-order-item.png)

  * ...be able to add a note to the kitchen or delivery.
  * ...choose time I expect to pick up the food or have it delivered.
    * On shopping cart page, there is a card showing order information where user can choose to either pickup or delivery, choose the date and time they expect the order to be done, and add a note to the kitchen or delivery.
    ![Order info cart](readme-assets/features/order-info-card.png)

  * ...easily enter personal information / delivery information / payment information.
  * ...pay for orders with my card in a safe and secured matter.
    * Checkout page contains a form where user can enter their personal information, delivery information and payment information. They are built with clean and simple design so that they are easy to use and navigate. The form is also responsive and adaptable to different screen sizes.
    * Payment is handled by Stripe API which is a popular and secured payment system. Webhooks are also set up as a safety measure so that the payment is processed and the order is placed once the payment is successful.
    ![Checkout form](readme-assets/features/checkout-buyer-details.png)
    ![Payment form](readme-assets/features/checkout-payment.png)
    
  * ...receive a confirmation from the shop that I have successfully or failed to create an order or pay.
    * Upon successfully paying the order, buyer is redirected to a success page where they can see once again the order details and the payment information. A confirmation email is also sent to the buyer.
    ![Success page](readme-assets/features/checkout-success.png)
    ![Success email](readme-assets/features/checkout-success-email.png)

### 4. As the shop owner, I want to:
  * ...be able to add more dishes to the menu.
  * ...be able to edit current dishes.
  * ...delete a dish out of the menu.
    * Django admin dashboard is set up with all CRUD possibility to manage and manipulate the database, including menu/product listing. With more time, a better admin dashboard with nicer user experience could have been implemented.
    ![Django admin dashboard](readme-assets/features/admin-dashboard.png)
    ![Admin product listing](readme-assets/features/admin-product-listing.png)

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
* A more custom designed page for admin dashboard could have been implemented in order to give shop owners a much better user experience in controlling and maintaining the database.