import {ProgressBar} from "react-bootstrap";
import PropTypes from "prop-types";

function CollectionStatus({status}) {
  const fraction = (status.totalTime !== 0.0) ? status.timeElapsed / status.totalTime : 0;
  const progress = Math.min(fraction * 100, 100);
  return (
    <>
      <ProgressBar now={progress} label={`${progress.toFixed(2)}%`} className="mt-3"/>
      <p className="mt-2">Lines collected: {status.linesCollected}</p>
    </>
  )
}

CollectionStatus.propTypes = {
  status: PropTypes.object.isRequired,
}

export default CollectionStatus;