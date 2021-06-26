# Database Interface

## Installation on Windows

### Apache Lounge to serve the files
1. Download Apache Lounge form [here]{https://www.apachelounge.com/download/}. I used version `httpd-2.4.48-win64-VS16.zip`
2. Unzip the file
3. Move the `Apache24` folder to `C:\Apache24`
4. Open the CMD __*with*__ admin rights
5. Run `cd C:\Apache24\bin httpd -k install` to install the service and allow all communication
6. Open the `C:\Apache24\conf\httpd.conf` file and insert
 
        Alias /images "C:/path/to/your/images"
        <Directory "C:/path/to/your/images">
            Options Indexes
            Require all granted
        </Directory>

    to map Paths to URLs

7. Open Services on windows and search for Apache24 and start the service
8. Yeay, you now have a running webserver!
9. (Optional) Run `ipconfig` in the CMD to find your Local IP address and access the server

### Frontend
1. If you have a browser, any browser, you are good

### Etc

you need to create a Config file called `database.ini` which looks something like this

        [mysql]
        host = localhost
        database = full_flake
        user = username
        password = password
        port = 3306
