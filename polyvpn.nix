{ lib
, buildPythonPackage
, fetchPypi

# build-system
, setuptools
, setuptools-scm

# dependencies
, requests
, beautifulsoup4

}:

buildPythonPackage rec {
  pname = "polyvpn-helper";
  version = "0.0.1";
  pyproject = true;

  src = ./. ;

  build-system = [
    setuptools
    setuptools-scm
  ];

  dependencies = [
    requests
    beautifulsoup4
  ];

  meta = {
    changelog = "";
    description = "";
    homepage = "https://github.com/namgo/polyvpn-helper";
    license = lib.licenses.gpl3;
    maintainers = with lib.maintainers; [ namgo ];
  };
}
