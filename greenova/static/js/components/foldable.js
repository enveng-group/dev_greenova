// Folds the element that is called
function foldElement(elem, display = "block") {
  // Check if element is good.
  if (!elem) {
    return false;
  }

  // Make sure the thing we're changing is an element, not the variable.
  let elemDisplay = elem.style.display;
  elem.style.display = (elemDisplay != 'none') ? 'none' : display;
  return true;
}
