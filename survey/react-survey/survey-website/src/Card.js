import React from 'react';
import Scene from './Scene';

function CardComponent(props) {
  var heightmap = `${process.env.PUBLIC_URL}/${props.heightmap}`; 
  return (
    <div className="card mb-4" onClick={props.onClick}>
      <div style={{height: '500px', width: '100%'}}>
        {/* Set the width and height of the Scene component to be 100% */}
        <Scene heightmapPath={heightmap} style={{width: '100%', height: '100%'}} />
      </div>
    </div>
  );
}

export default CardComponent;