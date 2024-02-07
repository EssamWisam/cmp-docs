import React, { useState, useEffect } from 'react';
import { LazyLoadImage } from 'react-lazy-load-image-component';

const LazyImage = ({ imageUrl, placeholderUrl, alt }) => {
    
    const [isValid, setIsValid] = useState(false);

      // Trigger the image check when the component mounts
        useEffect(() => {
            checkImage();
        }, [imageUrl]); // Add checkImage as a dependency for useEffect


    // Define checkImage as a useCallback to memoize it
    const checkImage = async () => {
        if (imageUrl === "") {
            setIsValid(false);
            return;
        }
        try {
            const response = await fetch(imageUrl);
            console.log(response.status);
            if (response.status === 200) {
                setIsValid(true);
            } else if (response.status === 403) {
                setIsValid(false);
            }
        } catch (error) {
            console.log("Error Caught!")
            setIsValid(false);
        }
    }

    return (
            <LazyLoadImage
                threshold={400}
                beforeLoad={checkImage}
                placeholderSrc={placeholderUrl}
                alt={alt}
                style={{ maxWidth: '100%', height: '150px', display: 'inline-block' }}
                src={isValid?imageUrl:placeholderUrl} // use normal <img> attributes as props
                />
    );

}

export default LazyImage;