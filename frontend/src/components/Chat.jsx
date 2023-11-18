import { useEffect, useState } from "react";
import { IoMdSend } from "react-icons/io";
import { BiBot, BiUser } from "react-icons/bi";
import "./chat.css";
import { AudioRecorder, useAudioRecorder } from "react-audio-voice-recorder";
import PopUp from "./PopUp";
import { RiFridgeFill } from "react-icons/ri";
import { MdPhotoCameraFront } from "react-icons/md";
import { SiCodechef } from "react-icons/si";

const Chat = () => {
  const [chat, setChat] = useState([]);
  const [inputMessage, setInputMessage] = useState("");
  const [botTyping, setbotTyping] = useState(false);
  const [cameraOn, setCameraOn] = useState(false);

  useEffect(() => {
    const request_temp = {
      sender: "bot",
      msg: "👋 Hello there! \n Welcome to our delightful RecipeBot – your culinary companion for all things delicious! 🍲✨ \n Whether you are in the mood for a culinary adventure or just a friendly chat, RecipeBot is here to make your day tastier and brighter.\n 📸 Take a selfie, and let RecipeBot analyze your mood to suggest the perfect recipe that fits your vibe! Feeling adventurous? Craving comfort? RecipeBot has you covered. \n 🥕 Snap a pic of the ingredients you have, and let RecipeBot work its magic. It will whip up a mouthwatering recipe tailored to your pantry, turning those random items into a gourmet masterpiece! \n 💬 Prefer the classic text or feel like having a chit-chat with a bot buddy? RecipeBot is all ears (well, virtually!) and is ready for a delightful conversation anytime. \n 🗣️ And if you're feeling a bit lazy, don't worry! You can even talk to RecipeBot using your voice – just say the magic word, and let the culinary journey begin. \n So, are you ready to spice up your life with some amazing recipes or just have a friendly chat? Say hello to RecipeBot and let the flavor adventure begin! 🌶️🍽️",
    };

    setChat([...chat, request_temp]);
  }, []);

  useEffect(() => {
    // const objDiv = document.getElementById("messageArea");
    // objDiv.scrollTop = objDiv.scrollHeight;

    setTimeout(() => {
      var objDiv = document.getElementById("messageArea");
      objDiv.lastChild.scrollIntoView({ behavior: "smooth" });
    }, 50);
  }, [chat]);

  const handleSubmit = (evt) => {
    evt.preventDefault();

    const request_temp = { sender: "user", msg: inputMessage };

    if (inputMessage !== "") {
      setChat((chat) => [...chat, request_temp]);
      setbotTyping(true);
      setInputMessage("");
      agentAPI(inputMessage);
    } else {
      window.alert("Please enter valid message");
    }
  };

  const agentAPI = async function handleClick(msg) {
    await fetch("", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        charset: "UTF-8",
      },
      credentials: "same-origin",
      body: JSON.stringify({ msg }),
    })
      .then((response) => response.json())
      .then((response) => {
        if (response) {
          const chatTemp = [];

          for (const { text, image } of response) {
            const msg = text || image || null;

            const response_temp = {
              sender: "bot",
              msg,
            };

            chatTemp.push(response_temp);
          }
          setChat((chat) => [...chat, ...chatTemp]);
          setbotTyping(false);
        }
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const recorderControls = useAudioRecorder();
  const addAudioElement = (blob) => {
    const url = URL.createObjectURL(blob);
    const audio = document.createElement("audio");
    audio.src = url;
    audio.controls = true;
    // capture audio playback and do something with it
    // audio.play();
  };

  return (
    <div>
      <div>{cameraOn ? <PopUp setCameraOn={setCameraOn} /> : null}</div>
      <div className="h-screen lg:px-60 lg:py-4 lg:bg-[url('./../public/background.jpg')]">
      {/* <img src='../background.jpg' width='300' alt="selfie" /> */}
        <div className="lg:rounded-lg lg:border-2 lg:border-black">
          <div className="bg-green-700 lg:rounded-t-lg h-[100px]">
            <h1 className="text-4xl text-center pt-4 font-bold text-slate-900">
              Hello Fresh 🍋
            </h1>
            {botTyping ? <h6 className="text-center">Bot Typing....</h6> : null}
          </div>
          <div
            className="h-[calc(100vh-200px)] lg:h-[calc(100vh-200px-30px)] p-4 overflow-y-auto bg-[#FFFFFF]"
            id="messageArea"
          >
            {chat.map((user, key) => (
              <div
                key={key}
                className={chat[key + 1]?.sender !== "bot" ? "mb-2" : undefined}
              >
                {user.sender === "bot" ? (
                  <div
                    className={
                      key === 0
                        ? "flex items-center gap-x-2 bg-slate-300 px-3 pt-3 rounded-t-lg pb-3 rounded-b-lg"
                        : chat[key + 1]?.sender !== "bot"
                        ? "flex items-center gap-x-2 bg-slate-300 px-3 pb-3 rounded-b-lg"
                        : "flex items-center gap-x-2 bg-slate-300 px-3 pb-3"
                    }
                  >
                    {chat[key - 1]?.sender !== "bot" ? (
                      <SiCodechef className="border-2 border-slate-900 rounded-full p-1 text-4xl min-w-[35px]" />
                    ) : (
                      <div className="pl-9" />
                    )}
                    <h5 className="bg-green-100 rounded-lg py-2 px-3">
                      {user.msg && /\bhttps?:\/\/\S+/i.test(user.msg) ? (
                        /\.(gif|jpe?g|tiff?|png|webp|bmp)$/i.test(user.msg) ? (
                          <img src={user.msg} alt="img" className="w-40" />
                        ) : (
                          <a
                            href={user.msg}
                            target="_blank"
                            rel="noopener noreferrer"
                          >
                            {user.msg}
                          </a>
                        )
                      ) : (
                        user.msg
                      )}
                      {user.buttons && (
                        <div className="space-x-2 pt-3">
                          {user.buttons.map((button, key) => (
                            <button
                              key={key}
                              className="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded-lg"
                              onClick={() => {
                                setbotTyping(true);
                                agentAPI(button.payload);
                              }}
                            >
                              {button.title}
                            </button>
                          ))}
                        </div>
                      )}
                    </h5>
                  </div>
                ) : (
                  <div className="flex justify-end items-center gap-x-2 bg-slate-300 px-3 pt-3 rounded-t-lg">
                    <h5 className="bg-yellow-100 rounded-lg py-2 px-3 mb-2">
                      {user.msg}
                    </h5>
                    <BiUser className="border-2 border-slate-900 rounded-full p-1 text-4xl min-w-[35px]" />
                  </div>
                )}
              </div>
            ))}
          </div>
          <div className="bg-green-700 lg:rounded-b-lg h-[100px] px-2 lg:px-40">
            <form
              className="flex items-center justify-center gap-x-2 h-full"
              onSubmit={handleSubmit}
            >
              <div>
                <AudioRecorder
                  onRecordingComplete={(blob) => addAudioElement(blob)}
                  recorderControls={recorderControls}
                />
                {/* <button onClick={recorderControls.stopRecording}>
                Stop recording
              </button> */}
              </div>
              <div className="h-1/2 w-full">
                <input
                  placeholder="Type your message here..."
                  onChange={(e) => setInputMessage(e.target.value)}
                  value={inputMessage}
                  type="text"
                  className="w-full h-full border-slate-900 rounded-lg p-2"
                ></input>
              </div>
              <div>
                <button
                  type="submit"
                  disabled={botTyping}
                  className="disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <IoMdSend className="border-2 border-slate-900 rounded-full p-1 text-4xl hover:bg-yellow-400 bg-green-500" />
                </button>
              </div>
              <div>
                <button
                  type="button"
                  className="disabled:opacity-50 disabled:cursor-not-allowed"
                  onClick={() => setCameraOn(true)}
                >
                  <MdPhotoCameraFront className="border-2 border-slate-900 rounded-full p-1 text-4xl hover:bg-yellow-400 bg-green-500" />
                </button>
                <button
                  type="button"
                  className="disabled:opacity-50 disabled:cursor-not-allowed"
                  onClick={() => setCameraOn(true)}
                >
                  <RiFridgeFill className="border-2 border-slate-900 rounded-full p-1 text-4xl hover:bg-yellow-400 bg-green-500" />
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Chat;
