import React, { useState, useEffect } from 'react';
import { useHistory } from "react-router-dom";
import { useParams } from "react-router-dom";
// yaml interaction
import yaml from 'js-yaml';
// switch
import DayNightToggle from 'react-day-and-night-toggle'
// icons
import * as MaterialDesign from "react-icons/md";
// sidebar tools
import { Menu, MenuItem, SubMenu, menuClasses} from 'react-pro-sidebar';
// themes and hex to rgba converter
import {themes, hexToRgba, saveSet, init} from './themes';

function SidebarGenerator({theme, setTheme, rtl, setRtl, setCurrentMarkdown, isGridPage, currentMarkdown}) {
    const [parsedData, setParsedData] = useState(null);
    const [language, setLanguage] = useState(init('language', 'عربي'))
    const [font, setFont] = useState(init('font', document.documentElement.style.getPropertyValue("--siteFont")))
    const history = useHistory();
    const { id } = useParams();

    useEffect(() => {
      // Fetch the YAML file using a relative path
      fetch('./department/sidebar.yaml')
        .then((response) => response.text())
        .then((data) => {
          // Parse the YAML data
          const parsedYaml = yaml.load(data);
          setParsedData(parsedYaml);
        })
        .catch((error) => {
          console.error('Error fetching or parsing YAML file:', error);
        });
    }, []);
  
    const menuItemStyles = {
      root: {
        fontSize: '13px',
        fontWeight: 400,
      },
      icon: {
        color: themes[theme].menu.icon,
        [`&.${menuClasses.disabled}`]: {
          color: themes[theme].menu.disabled.color,
        },
      },
      SubMenuExpandIcon: {
        color: '#b6b7b9',
      },
      subMenuContent: ({ level }) => ({
        backgroundColor:
          level === 0
            ? hexToRgba(themes[theme].menu.menuContent,  1)
            : 'transparent',
      }),
      
      button: {
        [`&.${menuClasses.disabled}`]: {
          color: themes[theme].menu.disabled.color,
        },
        '&:hover': {
          backgroundColor: hexToRgba(themes[theme].menu.hover.backgroundColor, 1),
          color: themes[theme].menu.hover.color,
        },
      },
      label: ({ open }) => ({
        fontWeight: open ? 600 : undefined,
      }),
    };

      useEffect(() => {
        document.documentElement.style.setProperty("--siteFont", font);

      }, [font]);
  
      const handleRTLChange = (e) => {
        if (language === 'English'){
          saveSet(setLanguage, 'language', 'عربي')
          saveSet(setRtl, 'rtl', false)
          saveSet(setFont, 'font', 'Montserrat')
        }
        else {
          saveSet(setLanguage, 'language', 'English')
          saveSet(setRtl, 'rtl', true)
          saveSet(setFont, 'font', 'Tajawal')
        }
      };
    
      useEffect(() => {
        const root = document.documentElement;
        root.style.setProperty('--primary-color', localStorage.getItem('primary') || '#f1f1f1');
        root.style.setProperty('--inverse-color', localStorage.getItem('inverse') || '#1d1d1d');
          document.body.style.backgroundColor = localStorage.getItem('background') ||'#202020';
          document.body.style.color = localStorage.getItem('color') ||'#f1f1f1 !important';
      }
      , [])

      // handle on theme change event
      const handleThemeChange = (e) => {
        const root = document.documentElement;
        if (theme==='dark'){
          saveSet(setTheme, 'theme', 'light')
          root.style.setProperty('--primary-color', '#1d1d1d'); localStorage.setItem("primary", '#1d1d1d');
          root.style.setProperty('--inverse-color', '#f1f1f1'); localStorage.setItem("inverse", '#f1f1f1');
          document.body.style.backgroundColor = '#ffffff';      localStorage.setItem("background", '#ffffff');
          document.body.style.color = '#1d1d1d !important';     localStorage.setItem("color", '#1d1d1d !important');
        }
        else{
          saveSet(setTheme, 'theme', 'dark')
          root.style.setProperty('--primary-color', '#f1f1f1'); localStorage.setItem("primary", '#f1f1f1');
          root.style.setProperty('--inverse-color', '#1d1d1d'); localStorage.setItem("inverse", '#1d1d1d');
          document.body.style.backgroundColor = '#202020';      localStorage.setItem("background", '#202020');
          document.body.style.color = '#f1f1f1 !important';     localStorage.setItem("color", '#f1f1f1 !important');
        }
      };
  
      useEffect(()=>{
        if(rtl && !id.includes('_ar'))
        {
          let ar_id = id.replace('_m', '_ar_m').replace('_y', '_ar_y');
          history.push(ar_id)
        }
        if(!rtl && id.includes('_ar')) {
          let en_id = id.replace('_ar_m', '_m').replace('_ar_y', '_y');
          history.push(en_id)
        }
      }, 
       //eslint-disable-next-line react-hooks/exhaustive-deps 
      [rtl])

    
    // Helper function to create a MenuItem
    const createMenuItem = (label, label_ar, icon, link, rtl) => {
      // Dynamically access the MaterialDesign component based on the icon variable handle_page_lang_change(rtl,  "../department/"+link)
      const IconComponent = MaterialDesign[icon];
      // link no md
      function get_link(link) {
      let new_link = link;
      if (rtl){
        new_link = new_link.replace(/\.md$/, '_ar.md');
        new_link = new_link.replace(/\.yaml$/, '_ar.yaml');
      }
      new_link = new_link.replace(/\.md$/, '_m').replace(/\.yaml$/, '_y').replace(/\//g, '-').toLowerCase();
      return new_link;
    }
      return (
          <MenuItem onClick={()=>{history.push(get_link(link))}} icon={<IconComponent size={20} />}>{(rtl)?label_ar:label}</MenuItem>
      );
    };
  
    // Helper function to create a SubMenu
    const createSubMenu = (label, label_ar, icon, items, rtl) => {
      const IconComponent = MaterialDesign[icon];
      return (
      <SubMenu label={(rtl)?label_ar:label} icon={<IconComponent size={20} />}>
        {items.map(({ label, label_ar, icon, link }) => createMenuItem(label, label_ar, icon, link, rtl))}
      </SubMenu>
      )
    };
  
  
  
    if (!parsedData) {
      return <div>Loading...</div>;
    }
  
  
    // Generate the JSX structure
    return (
      <nav style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
        <img src={parsedData.logoSrc} alt="logo" style={{ margin: '1rem 0rem' }} />
        <section style={{ flex: 1, marginBottom: '32px', overflow: "scroll" }}>
          {parsedData.sections.map(({ title, menu }) => (
            <>
            <div style={{ padding: '0 24px', marginBottom: '8px' }}>
              <h4 className="title" style={{ opacity: 0.7, letterSpacing: '0.7px', fontSize: '0.7rem' }}>
                {(rtl) ? title.label_ar : title.label}
              </h4>
            </div>
            <Menu menuItemStyles={menuItemStyles}>
              {menu.map(({ label, label_ar, icon, link, items }) =>
                items ? (
                  createSubMenu(label, label_ar, icon, items, rtl)
                ) : (
                  createMenuItem(label, label_ar, icon, link, rtl)
                )
              )}
            </Menu>
            </>
          ))}
        </section>
        <div style={{ marginBottom: '10px', display:'flex', flexDirection:'row', justifyContent:'space-around'}}>
              <div style={{ marginBottom: '10px', marginLeft: 13 }}>
                    <DayNightToggle
                      onChange={() => handleThemeChange()}
                      checked={theme === 'dark'}
                      shadows={false}
                    />
              </div>
              <div style={{ marginBottom: '10px', marginLeft: 13 }}  >
                <button onClick={handleRTLChange} id="rtl" style={{fontSize:'0.8rem', padding: '0.4rem 1.4rem', borderRadius:'1rem', border: 'none', cursor: 'pointer', backgroundColor:'#00C2CB'}}> {language} </button>
              </div>
          </div>
      </nav>
    );
  }
  export default SidebarGenerator;
  
  