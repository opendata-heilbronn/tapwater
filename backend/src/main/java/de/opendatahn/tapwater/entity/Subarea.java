package de.opendatahn.tapwater.entity;

import javax.persistence.*;

@Entity
public class Subarea {

		@Id
		@GeneratedValue
		private Long id;

	@Column(nullable = false)
	private String name;

	@ManyToOne
	private City city;

	public City getCity() {
		return city;
	}

	public void setCity(City city) {
		this.city = city;
	}

	public Long getId() {
		return id;
	}

	public void setId(Long id) {
		this.id = id;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}
}
