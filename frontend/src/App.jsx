import {useEffect, useState} from 'react';
import {Alert, Button, Container} from 'react-bootstrap';
import axios from "axios";

import Header from './components/Header';
import Footer from './components/Footer';
import VoxelSelector from './components/VoxelSelector';
import DurationInput from './components/DurationInput';
import CollectionStatus from "./components/CollectionStatus.jsx";

const BASE_URL = import.meta.env.VITE_BASE_URL;

function App() {
  const [activeBox, setActiveBox] = useState(null);
  const [duration, setDuration] = useState(30);
  const [customLabel, setCustomLabel] = useState('');
  const [alertMessage, setAlertMessage] = useState({
    message: '',
    variant: 'info',
  })
  const [collecting, setCollecting] = useState(false);
  const [status, setStatus] = useState({
    timeElapsed: 0.0,
    totalTime: 30.0,
    linesCollected: 0,
  })

  const toggleBox = (index) => {
    setActiveBox(index === activeBox ? null : index);
  };

  function handleSubmit() {
    if (activeBox === null) {
      setAlertMessage({
        message: 'Please select a voxel',
        variant: 'danger',
      })
      return;
    }

    let labelSuffix = customLabel.trim();
    if (labelSuffix !== '') {
      labelSuffix = `_${labelSuffix}`;
    }

    axios.post(`${BASE_URL}/collect`, {
      label: `voxel-${activeBox + 1}${labelSuffix}`,
      duration: duration,
    }, {
      timeout: 5000,
    }).then((response) => {
      setAlertMessage({
        message: response.data.message,
        variant: "info",
      })
      setCollecting(true);
    }).catch((error) => {
      if (error.response === undefined) {
        setAlertMessage({
          message: `Error connecting to the server, ${error.message}.`,
          variant: "danger",
        })
        return;
      }
      setAlertMessage({
        message: error.response.data.detail,
        variant: "danger",
      })
    });
  }

  useEffect(() => {
    let intervalId;
    if (collecting) {
      intervalId = setInterval(() => {
        axios.get(`${BASE_URL}/status`).then((response) => {
          setStatus(response.data);
          let collecting = response.data?.collecting
          if (!collecting) {
            setAlertMessage({
              message: "Data collection completed",
              variant: "success",
            })
          }
          setCollecting(collecting);
        });
      }, 2500);
    }

    return () => {
      clearInterval(intervalId);
    }
  }, [collecting]);

  return (
    <>
      <Header/>
      <Container className="my-5">
        {alertMessage.message !== '' && (
          <Alert
            variant={alertMessage.variant}
            onClose={() => setAlertMessage({message: "", variant: "info"})}
            dismissible
          >
            {alertMessage.message}
          </Alert>
        )}
        <VoxelSelector activeBox={activeBox} toggleBox={toggleBox}/>
        <DurationInput duration={duration} setDuration={setDuration}/>
        <input
          type="text"
          className="form-control mt-3"
          placeholder="Custom label"
          value={customLabel}
          onChange={(event) => setCustomLabel(event.target.value)}
        />
        <Button
          variant="primary"
          type="submit"
          className="mt-3"
          onClick={handleSubmit}
        >
          Submit
        </Button>
        {collecting && (<CollectionStatus status={status}/>)}
      </Container>
      <Footer/>
    </>
  );
}

export default App;