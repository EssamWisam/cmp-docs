import React, { useState } from 'react';
// components
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import PureModal from 'react-pure-modal';
import ImageComponent from './ImageComponent';
import 'react-pure-modal/dist/react-pure-modal.min.css';
// css
import './grid.css';
import './fireworks.css';   // for fireworks on hover

const GridGenerator = ({ jsonData, setHoverStatus, currentMarkdown }) => {
    // console.log(jsonData)
    const [modal, setModal] = useState(false);
    const [modalContent, setModalContent] = useState('');
  
    const openModal = (content) => {
      setModalContent(content);
      setModal(true);
    };
  
    const renderItems = (items) => {
      var mdCheck = currentMarkdown.includes("department/Extras/Classes");
      return items.map((item, index) => (
        <div className="course-circle" key={index} onClick={() => {openModal(item.markdown)}} onMouseEnter={() => {setHoverStatus(true)}} onMouseLeave={() => {setHoverStatus(false)}}>
          { mdCheck ?  
          <ImageComponent alt={item.name} imageUrl={item.image} placeholderUrl={`https://api.dicebear.com/7.x/thumbs/svg?mouth=variant1,variant2,variant3,variant4&seed=${item.name}&faceOffsetX=0&eyes=variant2W10,variant2W12,variant2W14,variant2W16,variant3W10,variant3W12,variant3W14,variant3W16,variant4W10,variant4W12,variant4W14,variant4W16,variant5W10,variant5W12,variant5W14,variant5W16,variant6W10,variant6W12,variant6W14,variant6W16,variant7W10,variant7W12,variant7W14,variant7W16,variant8W10,variant8W12,variant8W14,variant8W16,variant9W10,variant9W12,variant9W14,variant9W16`}></ImageComponent>
          :<img src={item.image.length > 0? item.image : `https://api.dicebear.com/7.x/thumbs/svg?mouth=variant1,variant2,variant3,variant4&seed=${item.name}&faceOffsetX=0&eyes=variant2W10,variant2W12,variant2W14,variant2W16,variant3W10,variant3W12,variant3W14,variant3W16,variant4W10,variant4W12,variant4W14,variant4W16,variant5W10,variant5W12,variant5W14,variant5W16,variant6W10,variant6W12,variant6W14,variant6W16,variant7W10,variant7W12,variant7W14,variant7W16,variant8W10,variant8W12,variant8W14,variant8W16,variant9W10,variant9W12,variant9W14,variant9W16`} alt={item.name} />}
          <p id="p">{item.name}</p>
        </div>
      ));
    };
  
    const renderSections = () => {
      return jsonData.map((section, index) => (
        <section key={index}>
          <h1>{section.title}</h1>
          <ReactMarkdown children={section.description} remarkPlugins={[remarkGfm]} />
          {section.items.map((item, itemIndex) => (
            <div key={itemIndex}>
              <h2>{item.title}</h2>
              <ReactMarkdown children={item.description} remarkPlugins={[remarkGfm]} />
              <div className="wrapped-circles">{renderItems(item.items)}</div>
            </div>
          ))}
        </section>
      ));
    };
    return (
      <div>
        {renderSections()}
        <PureModal
          header={jsonData[0].markdown_title}
          isOpen={modal}
          onClose={() => {
            setModal(false);
            setModalContent('');
          }}
          width={'800px'}
        >
          <ReactMarkdown children={modalContent} remarkPlugins={[remarkGfm]} />
        </PureModal>
       
      </div>
    );
  };
  export default GridGenerator;
  
  