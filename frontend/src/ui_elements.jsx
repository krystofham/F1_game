import React from 'react';
import { Link } from 'react-router-dom';
export function Herosection({isMobile}) {
  if (!isMobile){
  return (
    <>
      <HeroSectionDesktop />
    </>
  );}
  else {
    return (
    <>
      <HeroSectionMobile />
    </>
    );
  }
}

export function Navbar() {
    return (
        <nav>
            <Link to="/">Teams</Link>
            <Link to="/players">Drivers</Link>
        </nav>
    )
}

function HeroSectionMobile (){
    return(
    <>
    </>
    );
}
function HeroSectionDesktop (){
    return(
    <>
    </>
    );
}