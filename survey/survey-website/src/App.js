import React, { useState } from 'react';
import CardComponent from './Card';
import Scene from './Scene';
import { click } from '@testing-library/user-event/dist/click';

var clicks = 0;
var iterations = 0;
const indices = Array.from(Array(8).keys()).sort(() => Math.random() - 0.5);
const selection = [];

function App() {
  // Array of indices 0-7 for ids
  console.log("setting scene indices", clicks);
  const [scenes, setScenes] = useState([{id: clicks}, {id: clicks + 1}]);

  // Form data
  const [formData, setFormData] = useState({
    age: 0,
    profession: '',
    game_genre: '',
    game_hours: 0,
    answers: [],
  });

  const handleCardClick = (cardIndex) => {
    console.log(`Card ${cardIndex} clicked!`);
    console.log("clicks:", clicks);

    // If we haven't ran through all options, keep recording
    if (selection.length < indices.length / 2) {
      selection.push(scenes[cardIndex - 1].id);
      console.log("selection:", selection);
      setFormData({ ...formData, answers: selection });

      // Reorder scenes based on user's choice
      const chosenScene = scenes[cardIndex - 1];
      const otherScene = scenes.find((scene) => scene.id !== chosenScene.id);
      const chosenIndex = indices.indexOf(chosenScene.id);
      const otherIndex = indices.indexOf(otherScene.id);
      const newIndices = [...indices];
      newIndices[chosenIndex] = otherScene.id;
      newIndices[otherIndex] = chosenScene.id;
      setScenes([{ id: newIndices[clicks] }, { id: newIndices[clicks + 1] }]);
    }

    // While there's still images to present, update the cards
    if (clicks < indices.length - 2) {
      clicks = clicks + 2;
      setScenes([{ id: indices[clicks] }, { id: indices[clicks + 1] }]);
    } else {
      console.log("Finished!");
      handleNextClick();
    }
  };

  // Pagination state
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(3);

  // Form submission handler
  const handleSubmit = (event) => {
    event.preventDefault();
    console.log(formData);
    // POST fomData to server
    fetch('http://localhost:3000/api/survey', {
      method: 'POST',
      mode: 'cors',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log('Success:', data);
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  };

  // Form input change handler
  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData({ ...formData, [name]: value });
  };

  // Pagination button click handlers
  const handlePrevClick = () => {
    setCurrentPage(currentPage - 1);
  };

  const handleNextClick = () => {
    setCurrentPage(currentPage + 1);
  };

  // Render form fields for the current page
  const renderFormFields = () => {
    switch (currentPage) {
      case 1:
        return (
          <>
            <div className="form-group">
              <label htmlFor="name">Name</label>
              <input type="text" className="form-control" id="name" name="name" value={formData.name} onChange={handleChange} />
            </div>
            <div className="form-group">
              <label htmlFor="age">Age</label>
              <input type="number" className="form-control" id="age" name="age" value={formData.age} onChange={handleChange} />
            </div>
            <div className="form-group">
              <label htmlFor="game_genre">Game Genre</label>
              <input type="text" className="form-control" id="game_genre" name="game_genre" value={formData.game_genre} onChange={handleChange} />
            </div>
            <div className="form-group">
              <label htmlFor="game_hours">Game Hours per Week</label>
              <input type="number" className="form-control" id="game_hours" name="game_hours" value={formData.game_hours} onChange={handleChange} />
            </div>
          </>
        );
      case 2:
        return (
          <>
            <div className="container mt-4">
              <div className="row">
                <div className="col-md-6">
                  <CardComponent scenes={scenes} heightmap={`heightmap${scenes[0].id}.png`} onClick={() => handleCardClick(1)} />
                </div>
                <div className="col-md-6">
                  <CardComponent scenes={scenes} heightmap={`heightmap${scenes[1].id}.png`} onClick={() => handleCardClick(2)} />
                </div>
              </div>
            </div>
          </>
        );
      case 3:
        return (
          // Centered thank you message
          <div className="text-center">
            <h1>Thank you!</h1>
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="container mt-4">
      <header className="text-center mb-4">
        <h1>Survey</h1>
      </header>
      <form>
        {renderFormFields()}
        <div className="d-flex justify-content-between">
          {currentPage == 1 && <button type="button" className="btn btn-primary" onClick={handleNextClick}>Next</button>}
          {currentPage == 2 && <button type="button" className="btn btn-secondary" onClick={handlePrevClick}>Previous</button>}
          {currentPage == 3 && <button type="button" className="btn btn-primary" onClick={handleSubmit}>Submit</button>}
        </div>
      </form>
    </div>
  );
}

export default App;
