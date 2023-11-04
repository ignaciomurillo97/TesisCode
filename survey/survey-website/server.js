const express = require('express');
const cors = require('cors');
const app = express();

// CORS
app.use(cors());

// Mongoose connection
const mongoose = require('mongoose');
const mongo_url = 'mongodb://root:example@mongo:27017/'
mongoose.connect(mongo_url, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => console.log('MongoDB connected'))
  .catch(err => console.log('Could not connect to mongoDB {}: ', err));

// Define the model
const surveyResponseSchema = new mongoose.Schema({
    age: Number,
    profession: String,
    game_genre: String,
    game_hours: Number,
    answers: [String],
}, { timestamps: true }); 

const SurveyResponse = mongoose.model('SurveyResponse', surveyResponseSchema);

// Body parser
const bodyParser = require('body-parser');
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// Serve the React site
app.use(express.static('build'));

// API endpoint
app.get('/api/survey', (req, res) => {
  const responses = SurveyResponse.find({}).then((responses) => {res.json(responses)});
});

// Save survey response
app.post('/api/survey', (req, res) => {
  // Save the survey response to the database
  console.log("Received Survey Response:", req.body);
  const surveyResponse = new SurveyResponse(req.body);
  surveyResponse.save()
    .then(() => {
      console.log("Success! saved survey response");
      res.json({ success: true });
    })
    .catch(err => {
      // Log error
      console.log("Error saving survey response:", err);
      res.json({ success: false, error: err });
    });
});

// Start the server
const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});