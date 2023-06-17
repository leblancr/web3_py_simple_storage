// SPDX-License-Identifier: MIT

pragma solidity >0.6.0 <0.9.0;

contract SimpleStorage {
    uint256 favoriteNumber;

    struct Person {
        string name;  // 0
        uint256 favoriteNumber;  // 1
    }

    //Person public person = Person({name: 'Beau', favoriteNumber: 2});
    Person[] public people;
    mapping(string => uint256) public nameToFavoriteNumber;

    function store(uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber;
    }

    // view, pure = blue button
    function retrieve() public view returns(uint256) {
        return favoriteNumber;
    }

    function addPerson(string memory _name, uint256 _favoriteNumber)public{
        people.push(Person(_name, _favoriteNumber));
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }
}
