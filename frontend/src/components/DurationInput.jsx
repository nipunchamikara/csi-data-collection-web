import {Form, InputGroup} from 'react-bootstrap';
import PropTypes from "prop-types";

function DurationInput({duration, setDuration}) {
  return (
    <Form.Group controlId="duration" className="mt-3">
      <Form.Label>Time Duration</Form.Label>
      <InputGroup>
        <Form.Control
          type="number"
          value={duration}
          min={1}
          onChange={(e) => setDuration(Number(e.target.value))}
          placeholder="Enter duration"
        />
        <InputGroup.Text>
          seconds
        </InputGroup.Text>
      </InputGroup>
    </Form.Group>
  );
}

DurationInput.propTypes = {
  duration: PropTypes.number.isRequired,
  setDuration: PropTypes.func.isRequired,
}

export default DurationInput;