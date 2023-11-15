import React, { useState } from 'react';

const ImageComponent = ({ imageUrl, placeholderUrl, alt }) => {
  const [isValid, setIsValid] = useState(false);

  const checkImage = async () => {
    if(imageUrl === "")
      return;
    try {
      const response = await fetch(imageUrl);
      console.log(response)
      if (response.ok) {
        setIsValid(true);
      } else {
        setIsValid(false);
      }
    } catch (error) {
      setIsValid(false);
    }
  };

  // Trigger the image check when the component mounts
  React.useEffect(() => {
    checkImage();
  }, [imageUrl, checkImage]);

  return (
    <img
      src={isValid ? imageUrl : placeholderUrl}
      alt={alt}
      style={{ maxWidth: '100%', height: 'auto' }}
    />
  );
};

export default ImageComponent;
