import React from 'react'
import "./PopUp.css";
import Webcam from "react-webcam";
import { FaCamera } from "react-icons/fa";

const PopUp = (props) => {
    const { setCameraOn } = props;
    const videoConstraints = {
        width: 1280,
        height: 720,
        facingMode: "user",
      };

  return (
    <div className='overlay flex items-center justify-center'>
        <Webcam
          audio={false}
          height={720}
          screenshotFormat="image/jpeg"
          width={1280}
          videoConstraints={videoConstraints}
        >
          {({ getScreenshot }) => (
            <button
              onClick={() => {
                const imageSrc = getScreenshot();
                setCameraOn(false);
                // use imageSrc to get captured image and use it anywhere
                // console.log(imageSrc);
              }}
            >
              <FaCamera className="border-2 border-slate-900 rounded-full m-3 p-1 text-6xl hover:bg-yellow-400 bg-green-500" />
            </button>
          )}
        </Webcam>
    </div>
  )
};

export default PopUp;
