# Ashevenue

Ashevenue is a web-scraping application designed to gather and display local venue events in a sortable format. 
The app leverages several powerful technologies to perform web scraping and manage data effectively.

## ⚙️ Current Setup

- **Deployment**: Containerized using Docker and deployed on Render.
- **Scraping Technologies**: Uses Playwright for dynamic content scraping, Beautiful Soup for parsing HTML.
- **Backend**: Built with Flask and SQLAlchemy for data management.
- **Self-Updating**: Utilizes cron jobs to periodically ping backend routes and keep the data up to date.

## 📦 Planned Migration

We are planning to move Ashevenue to AWS to potentially improve the management and performance of dynamic content scraping. 
The migration aims to address the issue where Playwright's headless browser times out when locating dynamic content, 
although it functions correctly in local and Docker environments. 
AWS might offer better scalability and control to handle such dynamic scraping more effectively.

## 🛠 Technologies

- **Flask**: Web framework for Python, providing the backend services.
- **SQLAlchemy**: ORM for managing database operations.
- **Beautiful Soup**: Library for parsing HTML and extracting data.
- **Playwright**: Automation library for testing and scraping dynamic web content.
- **Docker**: Containerization platform to ensure consistency across environments.
- **Render**: Deployment platform for containerized applications.

## 📋 Features

- **Dynamic Scraping**: Retrieves and processes event data from various local venues.
- **Sortable Events Page**: Displays events in a sortable format for easy browsing using an optional date range
- **Automatic Updates**: Regularly updates data via cron jobs to keep the information current.

## 📅 Future Plans

- **AWS Migration**: Transition to AWS for better management of dynamic content scraping and overall application performance.
- **Potentially adding other venues**: Once the dynamic content issues have been resolved, I will resume adding more venues.
- **Potentially adding other TOWNS!**: If the desire is there, I may add other cities to the app, building on previous experience.
- **Improved error handling**: The big downside to a web-scraper like this is that if/when a website updates, the code sometimes breaks. I'd like to implement automatic messaging in the event of errors so I can remain vigilant with updates.

## 🚀 Usage

To run Ashevenue locally:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/ashevenue.git
2. cd ashevenue
3. Build the Docker Image:
      ```
   docker build -t ashevenue .
4. Run the docker build
   ```
   docker run -p 5000:5000 ashevenue
5. Access the app at http://localhost:5000.

💬 Issues
If you encounter any issues or have suggestions, please open an issue on the GitHub repository.

📚 License
This project is licensed under the MIT License.

Feel free to explore and contribute to the Ashevenue project. Your feedback and contributions are welcome!
