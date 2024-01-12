import React, { useState, useEffect } from 'react';
// yaml interaction
import yaml from 'js-yaml';
import MenuIcon from '@mui/icons-material/Menu';
// sidebar and grid
import { Sidebar } from 'react-pro-sidebar';
import SidebarGenerator from './SidebarGenerator';
import GridGenerator from './GridGenerator';
// markdown components
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
// themes and hex to rgba converter
import {themes, hexToRgba, saveSet, init} from './themes';
// css
import './hack.css';          // modifies some internal styles
// navigation
import { useParams } from "react-router-dom";

const Home = () => {
  const [toggled, setToggled] = useState(init('toggled', false));
  const [broken, setBroken] = useState(init('broken', false));
  const [rtl, setRtl] = useState(init('rtl', false));
  const [theme, setTheme] = useState(init('theme', 'dark'));
  const [markdown, setMarkdown] = useState(init('markdown', `Just loading...`));
  const [jsonData, setJsonData] = useState(init('jsonData', {}))
  const { id } = useParams();
  const [currentMarkdown, setCurrentMarkdown] = useState(init('currentMarkdown', `./department/Extras/About.md`));
  const [isGridPage, setIsGridPage] = useState(init('isGridPage', false));
  // when the page loads, setCurrentMarkdown
  useEffect(()=> {
    if(id!==undefined) {
    const file = id.replace(/_m/g, '.md').replace(/_y/g, '.yaml').replace(/-/g, '/');
    setCurrentMarkdown(`./department/${file}`);
    }
    else {
      setCurrentMarkdown(`./department/Extras/About.md`);
    }
  },[id]);

  useEffect(() => {
    fetch(currentMarkdown)
      .then((response) => response.text())
      .then((data) => {
        if(data.startsWith("<!DOCTYPE html>")){
          // throw an error
          throw new Error("could not load..")
        }
        if (currentMarkdown.endsWith('.md')) {
          saveSet(setIsGridPage, 'isGridPage', false)
          saveSet(setMarkdown, 'markdown', data);
        }
        else {
          saveSet(setJsonData, 'jsonData', yaml.load(data))
          saveSet(setIsGridPage, 'isGridPage', true)
        }
      })
      .catch((error) => {
        saveSet(setIsGridPage, 'isGridPage', false)
        saveSet(setMarkdown, 'markdown', (rtl) ? "هذه الصفحة غير موجودة بعد":"Page doesn't exist yet...");
        console.error('Error fetching or parsing the page file', error);
      });
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [currentMarkdown]);

  const [hoverStatus, setHoverStatus] = useState(false)

  return (
    <div style={{ display: 'flex', height: '100vh', direction: rtl ? 'rtl' : 'ltr', overflow: 'scroll' }}>
      <Sidebar
        toggled={toggled}
        width={"300px"}
        onBackdropClick={() => saveSet(setToggled, 'toggled', false)}
        onBreakPoint={setBroken}
        rtl={rtl}
        breakPoint="md"
        backgroundColor={hexToRgba(themes[theme].sidebar.backgroundColor, 1)}
        rootStyles={{
          color: themes[theme].sidebar.color,
        }}
      >
      <SidebarGenerator theme={theme} setTheme={setTheme} rtl={rtl} setRtl={setRtl} setCurrentMarkdown={setCurrentMarkdown} currentMarkdown={currentMarkdown} isGridPage={isGridPage}>
      </SidebarGenerator>
      </Sidebar>

      <main style={{color: (theme ==='dark')?'#fcfcfc':'#1d1d1d'}}>
        <div style={{ padding: '16px 24px', color: '#44596e' }}>
          <div style={{ marginBottom: '16px' }}>
            {broken && (
              <MenuIcon onClick={() => setToggled(!toggled)}/>
            )}
          </div>
        </div>
        <article style={{padding: '1.5rem', overflow: 'scroll', height: "calc(100% - 100px)"}}>
        <div class="pyro" style={{display:(isGridPage && (jsonData[0].markdown_title === "Student Info" || jsonData[0].markdown_title === "معلومات عن الطالب") && hoverStatus)?'block':'none'}}>
          <div class="before"></div>
          <div class="after"></div>
        </div>
        {(!isGridPage)?
        <ReactMarkdown children={markdown} remarkPlugins={[remarkGfm]} />
        :
        <GridGenerator jsonData={jsonData} setHoverStatus={setHoverStatus} currentMarkdown={currentMarkdown}/>
        }
        </article>
      </main>
    </div>
  );
};

export default Home;