- [Project Charter](#project-charter)
  * [Vision](#vision)
  * [Mission](#mission)
  * [Success riteria](#success-criteria)
- [Backlog](#backlog)
  * [Planning](#planning)
  * [Backlog](#backlog)
  * [Icebox](#icebox)
  
  ## Project Charter
### Vision
This project aims to connect local coffee producers with wholesale coffee suppliers. While there are numerous farms that are producing coffee, it might still be difficult for the wholesale business to learn about coffee producers and find the kind of coffee that the market wants. By introducing sources of high-qulity coffee beans to the market, the 'Bean!' application helps improve the lives of local coffee producers and contributes to a thriving coffee community.

### Mission
From the application interface, users can input their desired values of coffee bean attributes (aroma, acidicity, etc.), and then they will get a list of 10 coffee beans generated from the k-means algorithm using the data scraped from [the Coffee Quality Institute's review pages](https://database.coffeeinstitute.org/). The dataset contains reviews of 1312 arabica and 28 robusta coffee beans from the Coffee Quality Institute's trained reviewers, and users can directly contact the owners of high-quality arabica and robusta lots by following the links provided in the app.

### Success criteria
The k-means clustering models will be evaluated by comparing their sum of squares within clusters and sum of squares between clusters, and from the F and Silhouette plots. The optimal number of clusters will generate distinct groups that contains coffee beans with very similar attributes. After the best model is chosen, the business value of this application will be evaluated by the number of coffee lots that the app connects with the market. This application will be considered as a success if at least 10% of the coffee bean producers are contacted from the link in the app.


## Backlog
### Planning
- Initiative 1. Build clustering models.
  * Epic 1. Prepare the data for analysis.
    + Story 1. Download the data from [this Kaggle page](https://www.kaggle.com/volpatto/coffee-quality-database-from-cqi?select=merged_data_cleaned.csv).
    + Story 2. Clean the data and correct inconsistencies due to human recording.
    + Stroy 3. Setting up RDS to query from the app.
  * Epic 2. Conduct exploratory data analysis.
    + Story 1. Capture patterns within the data and have a basic idea of the key variables in the clustering analysis.
  * Epic 3. Develop and come up with the best clustering model.
    + Story 1. Train k-means clustering models and test different values of k based on SSW, SSB and F and Silhouette plots. 
    + Story 2. Train and test Gaussian mixture models with different values of k and variance type.
    + Story 3. Explain the clusters and make sure they are meaningful and valuable.
- Initiative 2. Create the app.
  * Epic 1. Build the interactive interface for the app.
    + Story 1. Design the layout of home page, user input page and the output list.
    + Story 2. Use S3 to store the data on AWS.
  * Epic 2. Integrate the model and develop the app with Flask.
- Initiative 3. Test the app.
  * Epic 1. Test the app's functionality.
  * Epic 2. Conduct A/B tests to evaluate the app's business value.

### Backlog
- Initiative1.epic1.story1 (1 of story points) 
- Initiative1.epic1.story2 (2 of story points) 
- Initiative1.epic2.story1 (1 of story points) 
- Initiative1.epic3.story1 (2 of story points) 
- Initiative1.epic3.story3 (0 of story points) 



### Icebox
- Initiative1.epic3.story2 (4 of story points) 
- Initiative2.epic1.story1
- Initiative2.epic1.story2
- Initiative2.epic2
- Initiative3.epic1
- Initiative3.epic2

** Explanation on the story points above:


0 points - quick chore; 1 point ~ 1 hour (small); 2 points ~ 1/2 day (medium); 4 points ~ 1 day (large); 8 points - big and needs to be broken down more when it comes to execution.
