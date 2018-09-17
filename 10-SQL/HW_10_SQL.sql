# Use sakila db
use sakila;

# 1a. Display the first and last names of all actors from the table actor.
SELECT first_name, last_name FROM actor;

# 1b. Display the first and last name of each actor in a single column in upper case letters. Name the column Actor Name.
SELECT UPPER(CONCAT(first_name, ' ', last_name)) AS 'Actor Name' FROM actor;

# 2a. You need to find the ID number, first name, and last name of an actor, of whom you know only the first name, "Joe." 
SELECT actor_id, first_name, last_name FROM actor WHERE first_name = "Joe";

# 2b. Find all actors whose last name contain the letters GEN:
SELECT first_name, last_name FROM actor WHERE last_name LIKE '%GEN%';

# 2c. Find all actors whose last names contain the letters LI. This time, order the rows by last name and first name, in that order:
SELECT first_name, last_name FROM actor WHERE last_name LIKE '%LI%'
ORDER BY last_name, first_name;

# 2d. Using IN, display the country_id and country columns of the following countries: Afghanistan, Bangladesh, and China:
SELECT country_id, country FROM country WHERE country IN ('Afghanistan', 'Bangladesh', 'China');

# 3a. create a column in the table actor named description and use the data type BLOB
ALTER TABLE actor
ADD COLUMN description blob;

# 3b. Very quickly you realize that entering descriptions for each actor is too much effort. Delete the description column.
ALTER TABLE actor
DROP COLUMN description;

# 4a. List the last names of actors, as well as how many actors have that last name.
SELECT last_name, COUNT(last_name) AS 'Number_of_Actors_With_This_Last_Name' 
FROM actor GROUP BY last_name;

# 4b. List last names of actors and the number of actors who have that last name, but only for names that are shared by at least two actors
SELECT last_name, COUNT(last_name) AS 'Number_of_Actors_with_This_Last_Name'
FROM actor GROUP BY last_name
HAVING Number_of_Actors_with_This_Last_Name >= 2;

# 4c. The actor HARPO WILLIAMS was accidentally entered in the actor table as GROUCHO WILLIAMS. Write a query to fix the record.
UPDATE actor
SET first_name = "HARPO"
WHERE first_name = "GROUCHO" AND last_name = "WILLIAMS";

# 4d. Perhaps we were too hasty in changing GROUCHO to HARPO. In a single query, if the first name of the actor is currently HARPO, change it to GROUCHO.
UPDATE actor
SET first_name = "GROUCHO"
WHERE first_name = "HARPO";

# 5a. You cannot locate the schema of the address table. Which query would you use to re-create it?
SHOW CREATE TABLE address;

# 6a. Use JOIN to display the first and last names, as well as the address, of each staff member. Use the tables staff and address:
SELECT staff.first_name, staff.last_name, address.address
FROM staff
INNER JOIN address ON staff.address_id=address.address_id;

# 6b. Use JOIN to display the total amount rung up by each staff member in August of 2005. Use tables staff and payment.
SELECT staff.first_name, staff.last_name, SUM(payment.amount) AS 'Total Amount'
FROM staff
INNER JOIN payment ON staff.staff_id=payment.staff_id
WHERE payment.payment_date LIKE '2005-08%'
GROUP BY staff.staff_id;

# 6c. List each film and the number of actors who are listed for that film. Use tables film_actor and film. Use inner join.
SELECT film.title, COUNT(film_actor.actor_id) AS 'Number of Actors' 
FROM film
INNER JOIN film_actor ON film.film_id=film_actor.film_id
GROUP BY film.title;

# 6d. How many copies of the film Hunchback Impossible exist in the inventory system?
SELECT title, COUNT(inventory.inventory_id) AS 'Number of copies in Inventory system'
FROM inventory
INNER JOIN film ON inventory.film_id=film.film_id
WHERE film.title = "HUNCHBACK IMPOSSIBLE";

# 6e. Using the tables payment and customer and the JOIN command, list the total paid by each customer. List the customers alphabetically by last name:
SELECT customer.first_name, customer.last_name, SUM(payment.amount) AS 'Total Amount Paid'
FROM customer
INNER JOIN payment ON customer.customer_id=payment.customer_id
GROUP BY payment.customer_id
ORDER BY customer.last_name;

# 7a. Use subqueries to display the titles of movies starting with the letters K and Q whose language is English.
SELECT title
FROM film
WHERE title LIKE 'K%' OR title LIKE 'Q%' AND language_id IN
(
	SELECT language_id
    FROM language
    WHERE name = "English"
);

# 7b. Use subqueries to display all actors who appear in the film Alone Trip.
SELECT first_name, last_name
FROM actor
WHERE actor_id IN
(
	SELECT actor_id
    FROM film_actor
    WHERE film_id IN
	(
		SELECT film_id
		FROM film
        WHERE title = "ALONE TRIP"
	)
);

# 7c. You want to run an email marketing campaign in Canada, for which you will need the names and email addresses of all Canadian customers. Use joins to retrieve this information.
SELECT customer.first_name, customer.last_name, customer.email, country.country
FROM customer 
INNER JOIN address ON customer.address_id=address.address_id
INNER JOIN city ON address.city_id=city.city_id
INNER JOIN country ON city.country_id=country.country_id WHERE country.country = "Canada";

# 7d. Identify all movies categorized as family films.
SELECT film.title, category.name
FROM film
INNER JOIN film_category ON film.film_id=film_category.film_id
INNER JOIN category ON film_category.category_id=category.category_id WHERE category.name = "Family";

# 7e. Display the most frequently rented movies in descending order.

SELECT title, COUNT(title) AS 'Times_Rented'
FROM film 
INNER JOIN inventory ON film.film_id=inventory.film_id
INNER JOIN rental ON inventory.inventory_id=rental.inventory_id
GROUP BY title
ORDER BY Times_Rented DESC;

# 7f. Write a query to display how much business, in dollars, each store brought in.

SELECT store.store_id, SUM(amount) AS 'Store Revenue'
FROM payment
INNER JOIN rental ON payment.rental_id=rental.rental_id
INNER JOIN inventory ON rental.inventory_id=inventory.inventory_id
INNER JOIN store ON inventory.store_id=store.store_id
GROUP BY store.store_id;

# 7g. Write a query to display for each store its store ID, city, and country.

SELECT store.store_id, city.city, country.country
FROM store
INNER JOIN address ON store.address_id=address.address_id
INNER JOIN city ON address.city_id=city.city_id
INNER JOIN country ON city.country_id=country.country_id;

# 7h. List the top five genres in gross revenue in descending order.

select category.name AS 'Genre', SUM(payment.amount) AS 'Gross_Revenue'
FROM payment
INNER JOIN rental ON payment.rental_id=rental.rental_id
INNER JOIN inventory ON rental.inventory_id=inventory.inventory_id
INNER JOIN film_category ON inventory.film_id=film_category.film_id
INNER JOIN category ON film_category.category_id=category.category_id
GROUP BY Genre
ORDER BY Gross_Revenue DESC;

# 8a. In your new role as an executive, you would like to have an easy way of viewing the Top five genres by gross revenue. Use the solution from the problem above to create a view.

CREATE VIEW top_five_genres AS
select category.name AS 'Genre', SUM(payment.amount) AS 'Gross_Revenue'
FROM payment
INNER JOIN rental ON payment.rental_id=rental.rental_id
INNER JOIN inventory ON rental.inventory_id=inventory.inventory_id
INNER JOIN film_category ON inventory.film_id=film_category.film_id
INNER JOIN category ON film_category.category_id=category.category_id
GROUP BY Genre
ORDER BY Gross_Revenue DESC
LIMIT 5;

# 8b. How would you display the view that you created in 8a?

SELECT * FROM top_five_genres;

# 8c. You find that you no longer need the view top_five_genres. Write a query to delete it.

DROP VIEW top_five_genres;


