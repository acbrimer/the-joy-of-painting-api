CREATE TABLE episodes (
        id CHAR(6) NOT NULL, 
        season INTEGER NOT NULL, 
        episode INTEGER NOT NULL, 
        title VARCHAR(255) NOT NULL, 
        painting_title VARCHAR(255), 
        painting_index INTEGER NOT NULL, 
        img_src VARCHAR, 
        youtube_src VARCHAR, 
        date DATE, 
        PRIMARY KEY (id)
)



CREATE TABLE colors (
        id CHAR(6) NOT NULL, 
        name VARCHAR(255) NOT NULL, 
        hex VARCHAR(7) NOT NULL, 
        PRIMARY KEY (id)
)



CREATE TABLE subjects (
        id VARCHAR(100) NOT NULL, 
        name VARCHAR(100) NOT NULL, 
        PRIMARY KEY (id)
)



CREATE TABLE episode_subjects (
        episode_id CHAR(6) NOT NULL, 
        subject_id VARCHAR(100) NOT NULL, 
        PRIMARY KEY (episode_id, subject_id), 
        FOREIGN KEY(episode_id) REFERENCES episodes (id), 
        FOREIGN KEY(subject_id) REFERENCES subjects (id)
)



CREATE TABLE painting_colors (
        episode_id CHAR(6) NOT NULL, 
        color_id CHAR(6) NOT NULL, 
        PRIMARY KEY (episode_id, color_id), 
        FOREIGN KEY(episode_id) REFERENCES episodes (id), 
        FOREIGN KEY(color_id) REFERENCES colors (id)
)