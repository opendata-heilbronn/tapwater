package de.opendatahn.tapwater.entity;

import javax.persistence.*;
import java.util.Date;

@Entity
public class Substance {

	@Id
	@GeneratedValue
	private Long id;

	@ManyToOne
	private Subarea subarea;

	private Date dataCollectedDate;

	private Double magnesium;

	public Long getId() {
		return id;
	}

	public void setId(Long id) {
		this.id = id;
	}

	public Subarea getSubarea() {
		return subarea;
	}

	public void setSubarea(Subarea subarea) {
		this.subarea = subarea;
	}

	public Date getDataCollectedDate() {
		return dataCollectedDate;
	}

	public void setDataCollectedDate(Date dataCollectedDate) {
		this.dataCollectedDate = dataCollectedDate;
	}

	public Double getMagnesium() {
		return magnesium;
	}

	public void setMagnesium(Double magnesium) {
		this.magnesium = magnesium;
	}
}
