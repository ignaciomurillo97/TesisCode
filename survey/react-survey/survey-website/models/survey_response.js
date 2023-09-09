// survey response mongoose schema
const mongoose = require('mongoose');

const surveyResponseSchema = new mongoose.Schema({
    age: Number,
    profession: String,
    game_genre: String,
    game_hours: Number,
    answers: [String],
}, { timestamps: true }); 

export default mongoose.model('SurveyResponse', surveyResponseSchema);