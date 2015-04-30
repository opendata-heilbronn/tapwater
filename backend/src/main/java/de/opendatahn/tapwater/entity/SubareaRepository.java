package de.opendatahn.tapwater.entity;

import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface SubareaRepository extends JpaRepository<Subarea, Long> {

	List<Subarea> findByCity(City city);

}
