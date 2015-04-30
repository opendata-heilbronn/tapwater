package de.opendatahn.tapwater.entity;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface CityRepository extends JpaRepository<City, Long> {

	List<City> findByName(@Param("name") String name);
}
