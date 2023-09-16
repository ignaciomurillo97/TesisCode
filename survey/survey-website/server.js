const express = require('express');
const app = express();

// Mongoose connection
const mongoose = require('mongoose');
mongoose.connect('mongodb://localhost:27017/test', { useNewUrlParser: true })
  .then(() => console.log('MongoDB connected'))
  .catch(err => console.log('Could not connect to mongoDB: ', err));

// Define the model
const surveyResponseSchema = new mongoose.Schema({
    age: Number,
    profession: String,
    game_genre: String,
    game_hours: Number,
    answers: [String],
}, { timestamps: true }); 

// Body parser
const bodyParser = require('body-parser');
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// Serve the React site
app.use(express.static('build'));

// API endpoint
app.get('/api/data', (req, res) => {
  // Return some sample data
  const data = {
    message: 'Hello, world!'
  };
  res.json(data);
});

const SurveyResponse = require('./models/survey_response');

// Save survey response
app.post('/api/survey_response', (req, res) => {
  // Save the survey response to the database
  const surveyResponse = new SurveyResponse(req.body);
  surveyResponse.save()
    .then(() => {
      res.json({ success: true });
    })
    .catch(err => {
      res.json({ success: false, error: err });
    });
});

// Start the server
const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});