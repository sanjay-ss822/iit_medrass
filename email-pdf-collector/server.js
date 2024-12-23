const express = require('express');
const mysql = require('mysql2');
const fs = require('fs');
const path = require('path');
const multer = require('multer');

const app = express();
const PORT = process.env.PORT || 3000;

// MySQL connection
const db = mysql.createConnection({
    host: 'localhost', // Your database host
    user: 'root', // Your database username
    password: 'siva', // Your database password
    database: 'pdf_uploads' // Your database name
});

// Connect to the database
db.connect(err => {
    if (err) {
        console.error('Database connection failed:', err.stack);
        return;
    }
    console.log('Connected to the database.');
});

// Set up storage for uploaded files
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, 'uploads/'); // Directory to save uploaded files
    },
    filename: (req, file, cb) => {
        cb(null, Date.now() + path.extname(file.originalname)); // Unique filename
    }
});

const upload = multer({ storage: storage });

// Create uploads directory if it doesn't exist
if (!fs.existsSync('uploads')) {
    fs.mkdirSync('uploads');
}

// Root route
app.get('/', (req, res) => {
    res.send('<h1>Welcome to the PDF Upload Service</h1><p>Use the /upload-pdf endpoint to upload your PDF files.</p>');
});

// Endpoint to handle PDF uploads
app.post('/upload-pdf', upload.single('pdf'), (req, res) => {
    if (!req.file) {
        return res.status(400).send('No file uploaded.');
    }

    const filename = req.file.filename;
    const filePath = req.file.path;

    // Store metadata in the database
    db.query('INSERT INTO documents (filename, file_path) VALUES (?, ?)', [filename, filePath], (err, results) => {
        if (err) {
            console.error('Error saving to database:', err);
            return res.status(500).send('Error saving to database.');
        }
        console.log(`Saved ${filename} to database.`);
        res.send('PDF uploaded successfully.');
    });
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});

// Endpoint to retrieve uploaded PDFs
app.get('/uploaded-pdfs', (req, res) => {
    db.query('SELECT * FROM documents', (err, results) => {
        if (err) {
            console.error('Error retrieving documents:', err);
            return res.status(500).send('Error retrieving documents.');
        }
        res.json(results); // Send the results as JSON
    });
});