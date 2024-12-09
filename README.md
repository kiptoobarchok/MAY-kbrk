## Messianic Assembly of Yahweh - KABOROK

- [project proposal](https://docs.google.com/document/d/1_ahp2PNbXBPoqhBHc8nvaHfmP5c3ARM2KYK3Sg5v3lQ/edit?tab=t.0)

- [Project Presentation](https://docs.google.com/presentation/d/1eplZX3N-fscSVEwZrf43O0c_vmLWj11VfdOtNl6TxFM/edit?usp=sharing)

<!-- ['!.may.png']() -->


## Team
- [KIPTOO CALEB](https://github.com/kiptoobarchok)

## Overview

This project aims to design and develop comprehensive and user-friendly website that caters to the needs of [Messianic Assembly of Yahweh - Kaborok](), offering an online platform for sharing church history, lessons, giving opportunities, and more. This website aims to enhance communication, community engagement, and facilitate smooth management of church information.

## Table of contents
- Contributors
- Features
- Technical features
- Technical stack
- Usage
<!-- - API Documentation -->


### Contributors
- [pst Eliud Chepkwony](https://wa.me/+254721544385)


### Features

1. Home page
```
- Theme of the year
- Vision
- Daily Verse
- visuals (pic)
```
2. User Authentication
```
- Sign up and log in management
- Account update options and personal details
```
3. Announcemnts
```
- central hub for all church-related updates, events, and notifications
- Add / update / delete announcement
```

4.  About Us
```
- Detailed history of the Messianic Assembly of Yahweh.
- Insight into the church's origins, values, and milestones.
- Emphasis on community growth and alignment with Yahweh’s commandments
```

### Future features addition
- Hebrew Calendar
- Media gallery
- Events and projects section

## Technical Features

- `Responsive Design`: Optimized for devices of all screen sizes using Bootstrap.

- `Dynamic Content`: Content is managed and rendered dynamically through Flask.

- `Profile Management`:
```
- Upload and display user profile pictures.
- Update personal information.
```
- `Database Integration`: Managed using SQLite for user and announcement storage.
- `Static Assets`:
```
- CSS for styling.
- Images for the church and user profiles.
```

## Tech Stack
- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, Bootstrap, jinja2
- **Database**: SQLite
- **Server**: Gunicorn for production deployment
- **Version Control**: Git

## Deployment
To run the website locally:
1. Clone the repo
```
git clone https://github.com/kiptoobarchok/MAY-kbrk
```

2. Navigation
```
cd  ~/MAY-kbrk
```
3. Install dependencies
```
pip install -r requirements.txt
```

4. Run the application
```
python run_app.py
```

5. Access the website
```
http://127.0.0.1:5555
```

### Future enhancements and ideas

- Integration of a blog for spiritual articles and teachings
- Addition of real-time chat for community interactions
- API endpoints for bible intergration
- Advanced search functionality for announcements and archives
- Lesson database
- Different locales for branches accessing the info specific to them

### Acknowledgement
- The development team of the Messianic Assembly of Yahweh - KABOROK.
- The community for their support and feedback.
