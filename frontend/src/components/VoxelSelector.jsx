import {Button, Col, FormLabel, Row} from 'react-bootstrap';
import PropTypes from "prop-types";

function VoxelSelector({activeBox, toggleBox}) {
  return (
    <Row>
      <FormLabel>Voxel</FormLabel>
      <>
        {[...Array(9).keys()].map((_, index) => (
          <Col key={index} xs={4} className="mb-3">
            <Button
              variant={activeBox === index ? 'primary' : 'secondary'}
              onClick={() => toggleBox(index)}
              className="w-100 fs-4" style={{height: '100px'}}
            >
              {index + 1}
            </Button>
          </Col>
        ))}
      </>
    </Row>
  );
}

VoxelSelector.propTypes = {
  activeBox: PropTypes.number,
  toggleBox: PropTypes.func.isRequired,
}

export default VoxelSelector;