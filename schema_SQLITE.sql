
CREATE TABLE episodes (
	id INTEGER NOT NULL, 
	season INTEGER, 
	title VARCHAR(255) NOT NULL, 
	youtube_url VARCHAR, 
	air_date DATE, 
	PRIMARY KEY (id)
)



CREATE TABLE colors (
	id INTEGER NOT NULL, 
	name VARCHAR(255) NOT NULL, 
	hex VARCHAR(7) NOT NULL, 
	PRIMARY KEY (id)
)



CREATE TABLE subjects (
	id INTEGER NOT NULL, 
	name VARCHAR(255) NOT NULL, 
	PRIMARY KEY (id)
)



CREATE TABLE paintings (
	id INTEGER NOT NULL, 
	episode_id INTEGER, 
	image_url VARCHAR, 
	title VARCHAR(255), 
	PRIMARY KEY (id), 
	FOREIGN KEY(episode_id) REFERENCES episodes (id)
)



CREATE TABLE episode_subjects (
	episode_id INTEGER NOT NULL, 
	subject_id INTEGER NOT NULL, 
	PRIMARY KEY (episode_id, subject_id), 
	FOREIGN KEY(episode_id) REFERENCES episodes (id), 
	FOREIGN KEY(subject_id) REFERENCES subjects (id)
)



CREATE TABLE painting_colors (
	painting_id INTEGER NOT NULL, 
	color_id INTEGER NOT NULL, 
	PRIMARY KEY (painting_id, color_id), 
	FOREIGN KEY(painting_id) REFERENCES paintings (id), 
	FOREIGN KEY(color_id) REFERENCES colors (id)
)


