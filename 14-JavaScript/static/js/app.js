// from data.js
var tableData = data;

// YOUR CODE HERE!

// create a function called Capitalize that will take in a string and capitalize first letter of each word in string
function Capitalize(str)
{
    // first take in passed-in string, lower case all letters and then split by whitespace
    lowercase_all = str.toLowerCase().split(' ');
    // use map to upper case at index 0 (ie first letter) and keep rest of index lowercase
    uppercase_first = lowercase_all.map((s) =>s.charAt(0).toUpperCase() + s.substring(1));
    // use join to put back together as string
    result = uppercase_first.join(' ');
    // return converted string
    return result;
}

// create function called makeTable that will make a table using HTML elements
// argument passed in is the array of data
function makeTable(tableData) {

// create variable called table_html that will be used to make the 
// UFO sightings table using Date, City, State, Country, Shape, Duration, and Comments
// data from data.js

// start with making table border
var table_html = "<table border='1|1'>";

// use for loop with tableData to bring in elements for Date, City, State, Country, Shape, Duration, and Comments
for (var i = 0; i < tableData.length; i++) {
    table_html+="<tr>";
    // add table data object and align in center for Date
    table_html+="<td align='center'>"+tableData[i].datetime+"</td>";
    // add table data object, align in center, and capitalize for City
    table_html+="<td align='center'>"+Capitalize(tableData[i].city)+"</td>";
    // add table data object, align in center, and upper case both letters for State
    table_html+="<td align='center'>"+tableData[i].state.toUpperCase()+"</td>";
    // add table data object, align in center, and upper case both letters for Country
    table_html+="<td align='center'>"+tableData[i].country.toUpperCase()+"</td>";
    // add table data object, align in center, and capitalize first letter for Shape
    table_html+="<td align='center'>"+Capitalize(tableData[i].shape)+"</td>";
    // add table data object and align in center for Duration
    table_html+="<td align='center'>"+tableData[i].durationMinutes+"</td>";
    // add table data object and align in center for Comments
    table_html+="<td align='center'>"+tableData[i].comments+"</td>";
    // end of row
    table_html+="</tr>";

}
// end of table creation
table_html+="</table>";
// create a full html variable to add column headers (Date, City, State, Country, Shape, Duration, Comments) to the table_html we just created
full_html = "<thead><tr><th>Date</th><th>City</th><th>State</th><th>Country</th><th>Shape</th><th>Duration</th><th>Comments</th></tr></thead>" + table_html;

// access by table id="ufo-table" from index.html file and populate with values from full_html variable
return document.getElementById("ufo-table").innerHTML = full_html;

}

// call function makeTable to render table on HTML page
makeTable(tableData);


// This is code that will listen for events and search through to find rows that match user input.
//
// Select the Filter Table button
var filterTable = d3.select("#filter-btn");

// Handler for when user clicks on Filter Table button
filterTable.on("click", function() {
    
    console.log("I am inside this click Filter Table button portion.")
    
    // Prevent the page from refreshing
    d3.event.preventDefault();

    // make filteredData a blank array to start
    var filteredData = [];
    console.log(filteredData);

    // Code for filtering by datetime when user enters text into the 'Enter a Date' text field
    //
    // Select the input element and get the raw HTML node
    var inputDateElement = d3.select("#datetime");
    // Get the value property of the input element
    var inputDateValue = inputDateElement.property("value");
    console.log(inputDateValue);
    console.log(tableData);
    // filter tableData and return only ones where datetime matches what the user entered in the 'Enter a Date' text field 
    var first_filteredData = tableData.filter(sighting => sighting.datetime === inputDateValue);
    console.log(first_filteredData);
    // push first_filteredData to filteredData array
    filteredData.push.apply(filteredData, first_filteredData);
     
    // Code for filtering by city when user enters text into the 'Enter a City' text field
    //
    // Select the input element and get the raw HTML node
    var inputCityElement = d3.select("#city");
    // Get the value property of the input element and make it lower case since values for city in data.js are lower case
    var inputCityValue = inputCityElement.property("value").toLowerCase();
    console.log(inputCityValue);
    // if inputCityValue is not blank (ie user did enter something into the 'Enter a City' text field)
    // then filter filteredData and return only ones where city matches what the user entered in the 'Enter a City' text field 
    if (inputCityValue !== "") {
        var filteredData = filteredData.filter(sighting => sighting.city === inputCityValue);
    };

    // Code for filtering by state when user enters text into the 'Enter a State' text field
    //
    // Select the input element and get the raw HTML node
    var inputStateElement = d3.select("#state");
    // Get the value property of the input element and make it lower case since values for state in data.js are lower case
    var inputStateValue = inputStateElement.property("value").toLowerCase();
    console.log(inputStateValue);
    // if inputStateValue is not blank (ie user did enter something into the 'Enter a State' text field)
    // then filter filteredData and return only ones where state matches what the user entered in the 'Enter a State' text field 
    if (inputStateValue !== "") {
        var filteredData = filteredData.filter(sighting => sighting.state === inputStateValue);
    };

    // Code for filtering by country when user enters text into the 'Enter a Country' text field
    //
    // Select the input element and get the raw HTML node
    var inputCountryElement = d3.select("#country");
    // Get the value property of the input element and make it lower case since values for country in data.js are lower case
    var inputCountryValue = inputCountryElement.property("value").toLowerCase();
    console.log(inputCountryValue);
    // if inputCountryValue is not blank (ie user did enter something into the 'Enter a Country' text field)
    // then filter filteredData and return only ones where country matches what the user entered in the 'Enter a Country' text field 
    if (inputCountryValue !== "") {
        var filteredData = filteredData.filter(sighting => sighting.country === inputCountryValue);
    };

    // Code for filtering by shape when user enters text into the 'Enter a Shape' text field
    //
    // Select the input element and get the raw HTML node
    var inputShapeElement = d3.select("#shape");
    // Get the value property of the input element and make it lower case since values for shape in data.js are lower case
    var inputShapeValue = inputShapeElement.property("value").toLowerCase();
    console.log(inputShapeValue);
    // if inputShapeValue is not blank (ie user did enter something into the 'Enter a Shape' text field)
    // then filter filteredData and return only ones where shape matches what the user entered in the 'Enter a Shape' text field 
    if (inputShapeValue !== "") {
        var filteredData = filteredData.filter(sighting => sighting.shape === inputShapeValue);
    };

    // Finally, call function makeTable to render the filteredData table on HTML page
    console.log(filteredData);
    makeTable(filteredData);

});




