# A clean architecture example in Python

This small project shows the implementation of a clean architecture in Python, according to what Robert Martin and others explain in some talks, articles and books like

* Hakka Labs: Robert "Uncle Bob" Martin - Architecture: The Lost Years https://www.youtube.com/watch?v=HhNIttd87xs
* Ruby Midwest 2011: Architecture the Lost Years by Robert Martin https://www.youtube.com/watch?v=WpkDN78P884
* The Clean Architecture https://blog.8thlight.com/uncle-bob/2012/08/13/the-clean-architecture.html
* DDD & Testing Strategy http://www.taimila.com/blog/ddd-and-testing-strategy/
* Jacobson Ivar, Christerson Magnus, Jonsson Patrik, Övergaard Gunnar, Object-Oriented Software Engineering - A Use Case Driven Approach, Addison-Wesley, 1992

The project implements a small search engine for artists.

Each artist is described by an UUID, gender, age, latitude, longitude and rate. The service must accept the following filtering criteria:
 
* an age range (minimum to maximum)
* location (latitude, longitude and radius)
* a rate threshold
* gender

The search criteria are all optional, but can be combined so that a request can have from zero to four criteria. Each criteria should also be able to have a rank/weight.

# Usage

* (Optional) Create a virtualenv with either Python 2 or Python 3: `virtualenv venv3 -p python3`
* Activate the virtualenv if you created one: `source venv3/bin/activate`
* Install the production requirements: `pip install -r requirements.txt`
* Run the web server: `./manage.py server`
* Access http://127.0.0.1:5000/artists in GET

If you want to develop or to test just install the relative requirements you can find in the `requirements` directory.

# Query parameters

The service accepts HTTP GET requests on the REST endpoint http://127.0.0.1:5000/artists with the following query parameters:

* `filter_age_min`, `filter_age_max`: integers
* `filter_location`: in the format `<longitude>,<latitude>,<radius>`, where the three values are float
* `filter_rate_max`: float
* `ranking_age`: a float representing the weight given to the distance of an artist from the average age of the resulting dataset (the higher the distance the lower the ranking).
* `ranking_location`: a float representing the weight given to the distance from the given location (the higher the distance the lower the ranking).
* `ranking_rate`: a float representing the weight given to the distance from the given rate threshold (the higher the distance the higher the ranking).

* Find all artists within a radius of 10 miles from London: http://127.0.0.1:5000/artists?filter_location=51.5126064,-0.1802461,10
* Find all artists between 34 years old and 45 years old: http://127.0.0.1:5000/artists?filter_age_min=34&filter_age_max=45
* Combine the previous two queries and rank artists considering the distance only: http://127.0.0.1:5000/artists?filter_location=51.5126064,-0.1802461,10&filter_age_min=34&filter_age_max=45&ranking_location=1
* Make the same query with a ranking based 80% on the distance and 20% on the age (distance from the average age): http://127.0.0.1:5000/artists?filter_location=51.5126064,-0.1802461,10&filter_age_min=34&filter_age_max=45&ranking_location=0.8&ranking_age=0.2
    

# Implementation notes

The main purpose of this project is to show a software _architecture_. The main advantages of this architecture are:

* Cleanliness: the project is cleary divided into several layers:
    * Domain: the representation of the domain model which is independent from the storage and the presentation layers
    * Use cases: the use cases implement the business logic, extracting data (made by domain models) from the service.
    * Repository: the implementation of a data repository (in this case a JSON file), which exposes an API shared by every repository, thus allowing to easily plug in a new data storage (such as a database, for example). 
    * Presentation: this layer transforms the results created by the use cases to match a given standard or format, such as REST, for example.  
* Testability: every layer is isolated and thus can be easily tested without the need of external systems (such as a database). The current test suite is made by 61 tests that run in 0.24 seconds, allowing the developer to work according to a strict TDD workflow (test first, code later).
* Adaptability: existing frameworks may be integrated in this architecture (Flask is being used in the current example to provide REST entry points), different databases (both SQL-based or with different approaches) or storage services may easily be integrated but also kept separated. The same happens with the UI, which may vary from a REST API to a console UI to a full-fledged Web UI.
 
Being this a demonstration project some choices have been made that should be reconsidered in a real-world project. Here you will find some considerations about those choices and the possible upgrades the code should get if used in a production environment.
 
* Lack of database: the only repository implemented in this project is ArtistJsonRepository, which is a file-based data storage. Obviously a production system shall implement an optimized data storage such as PostgreSQL, MongoDB, BigTable or other solutions.
* Ranking system: the ranking system has been implemented in the repository. It is used to order results in a non trivial way. This is something that may be discussed a lot, I think, in a real-world project. Strictly speaking the ranking system of a set of domain models should belong to the business rules, so should be implemented in the use case. Some parts of it, however, may be computationally intensive, so one could want to move the whole system to the repository, to take advantage of the particular external system and its optimizations. For example the repository could extract data from a cloud service that implements the ranking system in a very efficient way that cannot be offered by a local single process written in Python such as the use case is.
* Monolitc structure: to easily show the whole architecture all components have been packed into a single project. In a real world system teams or single developers shall be able to work on different parts of the system and release them without the need to put the whole codebase on a feature branch. The main layers that should be divided into isolated projects should be: the core domain code (domain/ and use_cases/), the repository interfaces (repositories/), that could also be split in different projects if more that one repository shall be actively maintained, the presentation layers (rest/), also possibly split in different projects if complex enough.

