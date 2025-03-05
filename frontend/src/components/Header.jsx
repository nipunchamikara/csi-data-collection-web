import {Container, Navbar} from 'react-bootstrap';

function Header() {
  return (
    <Navbar bg="dark" variant="dark">
      <Container>
        <Navbar.Brand>ESP32 CSI Collection</Navbar.Brand>
      </Container>
    </Navbar>
  );
}

export default Header;