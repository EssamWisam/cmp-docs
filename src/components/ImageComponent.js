import React, { useState, useEffect, useCallback } from 'react';

const ImageComponent = ({ imageUrl, placeholderUrl, alt }) => {
  const [isValid, setIsValid] = useState(false);

  // Define checkImage as a useCallback to memoize it
  const checkImage = useCallback(async () => {
    if(imageUrl === "")
      return;
    try {
      const response = await fetch(imageUrl);
      if (response.ok) {
        setIsValid(true);
      } else {
        setIsValid(false);
      }
    } catch (error) {
      setIsValid(false);
    }
  }, [imageUrl]); // Add imageUrl as a dependency for useCallback

  // Trigger the image check when the component mounts
  useEffect(() => {
    checkImage();
  }, [checkImage]); // Add checkImage as a dependency for useEffect

  return (
    <img
      src={isValid ? imageUrl : placeholderUrl}
      alt={alt}
      style={{ maxWidth: '100%', height: 'auto' }}
    />
  );
};

export default ImageComponent;
