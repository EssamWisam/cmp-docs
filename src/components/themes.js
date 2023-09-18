// not all colors here work; hence, the intervention in hack.css
export const themes = {
    light: {
      sidebar: {
        backgroundColor: '#fcfcfc',
        color: '#607489',
      },
      menu: {
        menuContent: '#fbfcfd',
        icon: '#57bfc9',
        hover: {
          backgroundColor: '#81D2D6',
          color: '#44596e',
        },
        disabled: {
          color: '#9fb6cf',
        },
      },
    },
  
    dark: {
      sidebar: {
        backgroundColor: '#1d1d1d',
        color: 'white !important',
      },
      menu: {
        menuContent: '#1d1d1d',
        icon: '#57bfc9',
        hover: {
          backgroundColor: '#00C2CB55',
          color: '#fcfcfc !important',
        },
        disabled: {
          color: '#3e5e7e',
        },
      },
    },
  };


  // hex to rgba converter
export const hexToRgba = (hex, alpha) => {
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);
  
    return `rgba(${r}, ${g}, ${b}, ${alpha})`;
  };
  

export const saveSet = (setter, name, value) => {
  function newSetter(item){
    setter(item);
    localStorage.setItem(name, JSON.stringify(item));
  }
  newSetter(value)
}
  

export const init = (key, defaultValue) => {
  const storedValue = localStorage.getItem(key);
  return storedValue ? JSON.parse(storedValue) : defaultValue;
};